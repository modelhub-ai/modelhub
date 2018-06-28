import subprocess
import os
import sys
from urllib import urlretrieve
from urllib2 import urlopen
import json
import argparse


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



def startBasic(model_name, docker_name):
    print ""
    print "============================================================"
    print "Model started."
    print "Open http://localhost:80/ in your web browser to access"
    print "modelhub web interface."
    print "Press CTRL+C to quit session."
    print "============================================================"
    print ""
    command = ("docker run --net=host -v " 
               + os.getcwd() + "/" + model_name + "/contrib_src:/contrib_src " 
               + docker_name)
    subprocess.check_call(command, shell = True)


def startExpert(model_name, docker_name):
    print ""
    print "============================================================"
    print "Modelhub Docker started in expert mode."
    print "Open the link displayed below to show jupyter dashboard and"
    print "open sandbox.ipynb for a prepared playground."
    print "Press CTRL+C to quit session."
    print "============================================================"
    print ""
    command = ("docker run --net=host -v " 
               + os.getcwd() + "/" + model_name + "/contrib_src:/contrib_src " 
               + docker_name + " jupyter notebook --allow-root")
    subprocess.check_call(command, shell = True)


def startBash(model_name, docker_name):
    print ""
    print "============================================================"
    print "Modelhub Docker started in interactive bash mode."
    print "You can freely explore the docker here."
    print "Press CTRL+D to quit session."
    print "============================================================"
    print ""
    command = ("docker run -it --net=host -v " 
               + os.getcwd() + "/" + model_name + "/contrib_src:/contrib_src " 
               + docker_name + " /bin/bash")
    subprocess.check_call(command, shell = True)


def startDocker(args, docker_name):
    if args.expert:
        startExpert(args.model, docker_name)
    elif args.bash:
        startBash(args.model, docker_name)
    else:
        startBasic(args.model, docker_name)


def download_github_dir(src_dir_url, branch_id, dest_dir):
    request_url = src_dir_url + "?ref=" + branch_id
    response = json.loads(urlopen(request_url).read())
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    for element in response:
        if element["type"] == "file":
            print element["name"], "-->", dest_dir
            src_file_url = element["download_url"]
            dest_file_path = os.path.join(dest_dir, element["name"])
            urlretrieve(src_file_url, dest_file_path)
        elif element["type"] == "dir":
            next_src_dir_url = src_dir_url + "/" + element["name"]
            next_dest_dir = os.path.join(dest_dir, element["name"])
            download_github_dir(next_src_dir_url, branch_id, next_dest_dir)



REQUEST_ROOT = "https://api.github.com/repos/modelhub-ai/modelhub/contents/models/"

def start(args):
    src_url = REQUEST_ROOT + args.model
    dest_dir = os.path.join(os.getcwd(), args.model)
    download_github_dir(src_url, "master", dest_dir)

    #startDocker(args, "modelhub/main_caffe2:0.1.0")



if __name__ == "__main__":
    try:
        args = parser.parse_args()
    except SystemExit as err: 
        if err.code == 2:
            parser.print_help()
        sys.exit(err.code)
    start(args)
