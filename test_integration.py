from __future__ import print_function
import subprocess
import os
import shutil
import sys
import traceback
import json
import argparse
import inspect
import jsonschema
import time
import numpy
try:
    # Python 2
    from urllib import urlretrieve
    from urllib2 import urlopen, HTTPError
except ImportError:
    # Python 3
    from urllib.request import urlopen, urlretrieve
    from urllib.error import HTTPError
from start import get_init_value


parser = argparse.ArgumentParser(description="Performs integration test for a modelhub model."\
                                             " This test performs a set of sanity checks to ensure the basic architeture of the model"\
                                             " complies to the modelhub model template and that the API calls to your model work."\
                                             " Run this test and make sure it passes before submitting a model to modelhub."\
                                             " NOTE: A passing test does not necessarily indicate that the model is working correctly."\
                                             " You should always also check manually if everything works as you expect."\
                                             " Especially test the prediction on a few sample datasets.",
                                formatter_class = argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("model", metavar = "MODEL", 
                    help = "Name of the model to run.")
parser.add_argument("-t", dest = "time", default = 5, type = int,
                    help = "Delay time (in seconds) to wait between starting the model and running the tests."\
                           " Sometimes a model's docker container needs more time to start and if the tests" \
                           " start before the docker is fully working, they will fail. In this case"\
                           " you should try to increase the delay time.")
parser.add_argument("-m", dest = "manual", action = "store_true",
                    help = "Given this option, the test does not start the corresponding model docker automatically."\
                           " Instead you have to start your model manually in a different terminal, using \"python start.py YOUR_MODEL_NAME\"."\
                           " This is helpful for debugging if the tests fail, so you can see the possible error output in the docker in the other terminal.")




count_warn = 0
test_fail = False

def warning(*message):
    """ 
    Call this function only directly from the test function for wich you want to signal 
    that it has passed but with a warning.
    """
    global count_warn
    count_warn += 1
    print("Integration test \"" + inspect.stack()[1][3] + "\" has PASSED with WARNING:")
    print("WARNING:", *message)


def error(*message):
    """ 
    Call this function only directly from the test function for wich you want to signal 
    that it has failed.
    """
    global test_fail
    test_fail = True
    msg = " ".join(message)
    exit_message = "Integration test \"" + inspect.stack()[1][3] + "\" has FAILED:"\
                   "\nERROR: " + msg
    sys.exit(exit_message)


def passed():
    """ 
    Call this function only directly from the test function for wich you want to signal 
    that it has passed.
    """
    print("Integration test \"" + inspect.stack()[1][3] + "\" has PASSED")


def get_api_response_as_json(api_call):
    try:
        return json.loads(urlopen(api_call).read())
    except HTTPError as e:
        if e.code == 400:
            return json.loads(e.read())
        else:
            raise


def _check_if_model_exists_locally(model_name):
    if not os.path.isdir(model_name):
        error("Model folder", model_name, "does not exist.")
    init_file = model_name + "/init/init.json"
    if not os.path.exists(init_file):
        error("Init file \"" + init_file + "\" for model", model_name, "does not exist.")
    return True


def check_if_model_exists_locally(model_name):
    if _check_if_model_exists_locally(model_name):
        passed()


def _count_docker_container_instances(model_name, docker_id):
    running_docker_images = subprocess.check_output("docker ps --format '{{.Image}}'", shell = True)
    running_docker_images = running_docker_images.strip().split('\n')
    count = running_docker_images.count(docker_id)
    return count


def check_if_docker_is_running(model_name):
    docker_id = get_init_value(model_name, "docker_id")
    count = _count_docker_container_instances(model_name, docker_id)
    if count < 1:
        error("Docker container", docker_id, "for", model_name, "is not running.",
              "Please make sure the image", docker_id, "exists and can be run.",
              "\nIf you started the integration test with the \"-m\" option, make sure the correct model docker is running"\
              " (you can start your model in another terminal via \"python start.py " + model_name + "\").")
    elif count > 1:
        error("Other modelhub Docker containers are currently running.",
              "For intergration testing please make sure that no modehub container is running when starting the test.")
    else:
        passed()


def check_if_config_complies_with_schema():
    with open("config_schema.json", "r") as f:
        schema_data = f.read()
    schema = json.loads(schema_data)
    config = get_api_response_as_json("http://localhost:80/api/get_config")
    if "error" in config:
        error(config["error"])
    try:
        jsonschema.validate(config, schema)
        passed()
    except jsonschema.exceptions.ValidationError as ve:
        error("The config file does not comply with the modelhub json schema. Validation error details:\n", str(ve))


def check_if_legal_docs_available():
    legal = get_api_response_as_json("http://localhost:80/api/get_legal")
    if "error" in legal:
        error(legal["error"])
    elif ("model_license" not in legal or legal["model_license"] == "") and \
         ("sample_data_license" not in legal or legal["sample_data_license"] == ""):
        warning("Licenses for model and sample data are missing.")
    elif "model_license" not in legal or legal["model_license"] == "":
        warning("License for model is missing.")
    elif "sample_data_license" not in legal or legal["sample_data_license"] == "":
        warning("License for sample data is missing.")
    else:
        passed()


def check_if_sample_data_available():
    samples = get_api_response_as_json("http://localhost:80/api/get_samples")
    if "error" in samples:
        error(samples["error"])
    elif len(samples) == 0:
        warning("No sample data found. Please consider providing sample data with your model.")
    else:
        passed()


def _get_output_types_from_config():
    model_io = get_api_response_as_json("http://localhost:80/api/get_model_io")
    output_types = [o["type"] for o in model_io["output"]]
    return output_types


def _is_output_vector_valid(def_shape, array):
    array = numpy.asarray(array)
    if (len(def_shape) != len(array.shape)) or (len(def_shape) != 1):
        return False
    if def_shape[0] != array.shape[0]:
        return False
    else:
        return True


def _is_output_matrix_valid(def_shape, array):
    array = numpy.asarray(array)
    if len(def_shape) != len(array.shape):
        return False
    for i, dim in enumerate(def_shape):
        if dim != array.shape[i]:
            return False
    else:
        return True


def check_if_prediction_returns_expected_data_format():
    samples = get_api_response_as_json("http://localhost:80/api/get_samples")
    if ("error" in samples) or (len(samples) == 0):
        warning("Cannot test prediction without sample data.")
        return
    sample_file = samples[0].rsplit("/", 1)[-1]
    config_output_types = _get_output_types_from_config()    
    result = get_api_response_as_json("http://localhost:80/api/predict_sample?filename=" + sample_file)
    if "error" in result:
        error(result["error"])
    if len(result["output"]) != len(config_output_types):
        error("Number of results does not match specified number of outputs in config.")
    for i, output in enumerate(result["output"]):
        if output["type"] != config_output_types[i]:
            error("Result type for output ", str(i), " does not match output type in config (" + output["type"],
                  "!=", config_output_types[i] + ")")
        if output["type"] == "label_list":
            for element in output["prediction"]:
                if ("probability" not in element) or ("label" not in element):
                    error("Format of output", str(i), "does not match output type defined in config.")
        elif output["type"] == "vector":
            if not _is_output_vector_valid(output["shape"], output["prediction"]):
                error("Shape of output", str(i), "is not valid, or output is not a vector")
        elif output["type"] in ["mask_image", "heatmap", "image", "custom"]:
            if not _is_output_matrix_valid(output["shape"], output["prediction"]):
                error("Shape of output", str(i), "is not valid, or output is not a matrix")
        else:
            error("Output type \"" + output["type"] + "\" is not a valid output type.")
    passed()    


def print_test_summary():
    if test_fail:
        print("\nIntegration test FAILED. See details above.")
    elif count_warn == 0:
        print("\nAll integration tests have PASSED.")
    else:
        print("\nThe integration tests have PASSED with", count_warn, "WARNINGS.",
              "Please consider fixing all warnings before submitting your model to modelhub.ai.")


def start_docker(args):
    if not args.manual:
        print("Starting", args.model, "docker under name modelhub_ai_test_container")
        if _check_if_model_exists_locally(args.model):
            docker_id = get_init_value(args.model, "docker_id")
            if _count_docker_container_instances(args.model, docker_id) > 0:
                raise RuntimeError("Other modelhub Docker containers are currently running.\n"\
                                   "For intergration testing please make sure that no other modehub container is running when starting the test.")
            command = ("docker run -d --rm --net=host --name=modelhub_ai_test_container -v " 
                    + os.getcwd() + "/" + args.model + "/contrib_src:/contrib_src " 
                    + docker_id)
            subprocess.check_call(command, shell = True)
            time.sleep(args.time)
    else:
        pass
    

def run_tests(args):
    print("")
    check_if_model_exists_locally(args.model)
    check_if_docker_is_running(args.model)
    check_if_config_complies_with_schema()
    check_if_legal_docs_available()
    check_if_sample_data_available()
    check_if_prediction_returns_expected_data_format()


def kill_docker(args):
    if not args.manual:
        print("\nShutting down", args.model, "docker")
        command = ("docker kill modelhub_ai_test_container")
        try:
            subprocess.check_call(command, shell = True)
        except Exception:
            print(traceback.format_exc())
            print("Failed to shut down docker. Probably it failed because it did not start correctly. Use the \"docker ps -a\" command to check if the modelhub_ai_test_container still exists and if it does, remove it.")
    else:
        pass


if __name__ == "__main__":
    args = parser.parse_args()
    try:
        start_docker(args)
        run_tests(args)
    except SystemExit as e: 
        test_fail = True
        print(e)
    except Exception:
        test_fail = True
        print(traceback.format_exc())
    finally:
        kill_docker(args)
        print_test_summary()
        

