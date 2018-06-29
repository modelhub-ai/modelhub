from __future__ import print_function
import subprocess
import os
import sys
import json
import argparse
try:
    # Python 2
    from urllib import urlretrieve
    from urllib2 import urlopen, HTTPError
except ImportError:
    # Python 3
    from urllib.request import urlopen, urlretrieve
    from urllib.error import HTTPError



parser = argparse.ArgumentParser(description="Starts model with modehub framework and downloads model and prerequisites"\
                                             " if they don't exist yet."\
                                             " By default starts a webservice showing details about the model providing"\
                                             " an easy user interface to run inference.")
parser.add_argument("model", metavar = "MODEL", 
                    help = "Name of the model to run.")
group = parser.add_mutually_exclusive_group()
group.add_argument("-e", "--expert", 
                    help = "Start in expert mode. Provides a jupyter notebook environment to experiment.",
                    action = "store_true")
group.add_argument("-b", "--bash", 
                    help = "Start modelhub Docker in bash mode. Explore the Docker on your own.",
                    action = "store_true")



def start_basic(model_name, docker_id):
    print("")
    print("============================================================")
    print("Model started.")
    print("Open http://localhost:80/ in your web browser to access")
    print("modelhub web interface.")
    print("Press CTRL+C to quit session.")
    print("============================================================")
    print("")
    command = ("docker run --net=host -v " 
               + os.getcwd() + "/" + model_name + "/contrib_src:/contrib_src " 
               + docker_id)
    subprocess.check_call(command, shell = True)


def start_expert(model_name, docker_id):
    print("")
    print("============================================================")
    print("Modelhub Docker started in expert mode.")
    print("Open the link displayed below to show jupyter dashboard and")
    print("open sandbox.ipynb for a prepared playground.")
    print("Press CTRL+C to quit session.")
    print("============================================================")
    print("")
    command = ("docker run --net=host -v " 
               + os.getcwd() + "/" + model_name + "/contrib_src:/contrib_src " 
               + docker_id + " jupyter notebook --allow-root")
    subprocess.check_call(command, shell = True)


def start_bash(model_name, docker_id):
    print("")
    print("============================================================")
    print("Modelhub Docker started in interactive bash mode.")
    print("You can freely explore the docker here.")
    print("Press CTRL+D to quit session.")
    print("============================================================")
    print("")
    command = ("docker run -it --net=host -v " 
               + os.getcwd() + "/" + model_name + "/contrib_src:/contrib_src " 
               + docker_id + " /bin/bash")
    subprocess.check_call(command, shell = True)


def start_docker(args):
    docker_id = get_init_value(args.model, "docker_id")
    if args.expert:
        start_expert(args.model, docker_id)
    elif args.bash:
        start_bash(args.model, docker_id)
    else:
        start_basic(args.model, docker_id)


def download_github_dir(src_dir_req_url, branch_id, dest_dir):
    request_url = src_dir_req_url + "?ref=" + branch_id
    response = json.loads(urlopen(request_url).read())
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    for element in response:
        if element["type"] == "file":
            src_file_url = element["download_url"]
            dest_file_path = os.path.join(dest_dir, element["name"])
            print(src_file_url, "\n-->", dest_file_path)
            urlretrieve(src_file_url, dest_file_path)
        elif element["type"] == "dir":
            next_src_dir_req_url = src_dir_req_url + "/" + element["name"]
            next_dest_dir = os.path.join(dest_dir, element["name"])
            download_github_dir(next_src_dir_req_url, branch_id, next_dest_dir)


def download_external_files(external_files, model_dir):
    for element in external_files:
        src_file_url = element["src_url"]
        dest_file_path = os.path.join(model_dir, element["dest_file_path"].strip("/"))
        if not os.path.exists(os.path.dirname(dest_file_path)):
            os.makedirs(os.path.dirname(dest_file_path))
        print(src_file_url, "\n-->", dest_file_path)
        urlretrieve(src_file_url, dest_file_path)


def get_model_req_url(model_name):
    request_root = "https://api.github.com/repos/modelhub-ai/modelhub/contents/models/"
    return request_root + model_name


def get_init_value(model_name, key):
    init_file_req_url = get_model_req_url(model_name) + "/init/init.json?ref=master"
    response = json.loads(urlopen(init_file_req_url).read())
    init = json.loads(urlopen(response["download_url"]).read())
    return init[key]


def download_model(model_name, dest_dir):
    github_branch_id = get_init_value(model_name, "branch_id")
    model_req_url = get_model_req_url(model_name)
    download_github_dir(model_req_url, github_branch_id, dest_dir)
    external_contrib_files = get_init_value(model_name, "external_contrib_files")
    download_external_files(external_contrib_files, dest_dir)


def download_model_if_necessary(model_name):
    model_dir = os.path.join(os.getcwd(), model_name)
    if os.path.exists(model_dir):
        print("Model folder exists already. Skipping download.")
    else:
        print("Downloading model ...")
        download_model(model_name, model_dir)
        print("Model download DONE!")



def start(args):
    download_model_if_necessary(args.model)
    start_docker(args)



if __name__ == "__main__":
    try:
        args = parser.parse_args()
    except SystemExit as e: 
        if e.code == 2:
            parser.print_help()
        sys.exit(e.code)
    try:
        start(args)
    except HTTPError as e:
        print("ERROR: Model download failed. Please check if this is a valid model name. Also, please check your internet connection. The model folder \"" + args.model + "\" is possibly corrupt. Please delete it (if it exists).")
        print("ERROR DETAIL: ", e)

