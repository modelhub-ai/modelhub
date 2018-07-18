from __future__ import print_function
import subprocess
import os
import shutil
import sys
import json
import argparse
import inspect
import jsonschema
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
                                             " Especially test the prediction on a few sample datasets.")
parser.add_argument("model", metavar = "MODEL", 
                    help = "Name of the model to run.")



count_warn = 0

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


def check_if_docker_is_running(model_name):
    docker_id = get_init_value(model_name, "docker_id")
    running_docker_images = subprocess.check_output("docker ps --format '{{.Image}}'", shell = True)
    running_docker_images = running_docker_images.strip().split('\n')
    count = running_docker_images.count(docker_id)
    if count < 1:
        error("Docker container", docker_id, "for", model_name, "is not running. Please start", model_name, 
              "in a different terminal with the modelhub start script: \"python start.py " + model_name + "\".")
    elif count > 1:
        error("Multiple modelhub Docker containers are currently running.",
              "For intergration testing please make sure that only the", model_name, "container is running")
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


def print_test_summary():
    if count_warn == 0:
        print("\nAll integration tests have PASSED.")
    else:
        print("\nThe integration tests have PASSED with", count_warn, "WARNINGS.",
              "Please consider fixing all warnings before submitting your model to modelhub.ai.")


def run_tests(args):
    check_if_docker_is_running(args.model)
    check_if_config_complies_with_schema()



if __name__ == "__main__":
    args = parser.parse_args()
    try:
        run_tests(args)
        print_test_summary()
    except (SystemExit, Exception) as e: 
        print(e)
        print("\nIntegration test FAILED. See details above.")
