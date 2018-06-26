#!/bin/bash

declare -r dockerIdentifier="modelhub/main_keras_2.0.2:0.1.0"
declare -r commitId="master"
declare -r serverAddress="https://raw.githubusercontent.com/modelhub-ai/modelhub/""$commitId""/models/"
declare -r modelIdentifier="cardiacfcn"
declare -a -r requiredFiles=("$modelIdentifier""/contrib_src/fcn_model.py"
                             "$modelIdentifier""/contrib_src/inference.py"
                             "$modelIdentifier""/contrib_src/postprocessing.py"
                             "$modelIdentifier""/contrib_src/preprocessing.py"
                             "$modelIdentifier""/contrib_src/run.py"
                             "$modelIdentifier""/contrib_src/sandbox.ipynb"
                             "$modelIdentifier""/contrib_src/license/model"
                             "$modelIdentifier""/contrib_src/license/sample_data"
                             "$modelIdentifier""/contrib_src/model/config.json"
                             "$modelIdentifier""/contrib_src/model/model.h5"
                             "$modelIdentifier""/contrib_src/model/weights.h5"
                             "$modelIdentifier""/contrib_src/sample_data/P01-0080.png"
                             "$modelIdentifier""/contrib_src/sample_data/P02-0140.png"
                             "$modelIdentifier""/contrib_src/sample_data/P03-0088.png"
                             "$modelIdentifier""/contrib_src/sample_data/P04-0160.png"
                             "$modelIdentifier""/contrib_src/sample_data/P05-0100.png"
                             "$modelIdentifier""/contrib_src/sample_data/P06-0108.png"
                             "$modelIdentifier""/contrib_src/sample_data/P07-0127.png"
                             "$modelIdentifier""/contrib_src/sample_data/P08-0140.png"
                             "$modelIdentifier""/contrib_src/sample_data/P09-0160.png"
                             "$modelIdentifier""/contrib_src/sample_data/P10-0087.png"
                             "$modelIdentifier""/contrib_src/sample_data/P11-0100.png"
                             "$modelIdentifier""/contrib_src/sample_data/P12-0088.png"
                             "$modelIdentifier""/contrib_src/sample_data/P13-0180.png"
                             "$modelIdentifier""/contrib_src/sample_data/P14-0120.png"
                             "$modelIdentifier""/contrib_src/sample_data/P15-0060.png"
                             "$modelIdentifier""/contrib_src/sample_data/P16-0040.png"
                             )


# ---------------------------------------------------------
# Process commandline parameters
# ---------------------------------------------------------
function printArgUsageAndExit()
{
    echo "Starts model with modehub framework and downloads model and prerequisites"
    echo "if they don't exist yet."
    echo ""
    echo "By default starts a webservice showing details about the model providing"
    echo "an easy user interface to run inference."
    echo ""
    echo "Usage: ./start_<modelname>.sh [option]"
    echo ""
    echo "  available options (select only one or none):"
    echo "    -e, --expert   Start in expert mode. Provides a jupyter notebook"
    echo "                   environment to experiment."
    echo "    -b, --bash     Start modelhub Docker in bash mode. Explore the Docker"
    echo "                   on your own."
    echo "    -h, --help     Print this help."

    exit 1
}

MODE="basic"
if [ $# = 1 ]; then
    key="$1"
    case $key in
        -e|--expert) MODE="expert";;
        -b|--bash) MODE="bash";;
        *|-h|--help) printArgUsageAndExit;;
    esac
elif [ $# -gt 1 ]; then
    printArgUsageAndExit
fi

# ---------------------------------------------------------
# Check prerequisites
# ---------------------------------------------------------

# checking if Docker exists
if ! command -v docker >/dev/null 2>&1; then
    echo >&2 "Docker is required to run models from modelhub. Please go to https://docs.docker.com/install/ and follow the instructions to install Docker on your system."
    exit 1
fi

# get the required modelhub Docker image
echo "Getting modelhub Docker image for $modelIdentifier"
docker pull "$dockerIdentifier"

# check if model data already exists
modelFolderExists=true
if ! [ -d "$modelIdentifier" ]; then
    modelFolderExists=false
fi

# try to download data if model folder does not exist
if [ "$modelFolderExists" = false ]; then
    # trying to get model data with curl
    echo "$modelIdentifier model data folder does not exist yet."
    if command -v curl >/dev/null 2>&1; then
        echo "Getting model data with curl"
        for file in "${requiredFiles[@]}"
        do
          mkdir -p $(dirname "$file")
          curl "$serverAddress""$file" --output "$file"
        done
    elif command -v wget >/dev/null 2>&1; then
        echo "Getting model data with wget"
        for file in "${requiredFiles[@]}"
        do
          mkdir -p $(dirname "$file")
          wget -O "$file" "$serverAddress""$file"
        done
    else
        echo >&2 "cURL or Wget are required to download the model data from modelhub. Please install either of them and run this script again."
        exit 1
    fi
    echo "Done getting model data."
else
    echo "Existing model data found."
fi


# ---------------------------------------------------------
# Run model
# ---------------------------------------------------------
function runBasic()
{
    echo ""
    echo "============================================================"
    echo "Model started."
    echo "Open http://localhost:80/ in your web browser to access"
    echo "modelhub web interface."
    echo "Press CTRL+C to quit session."
    echo "============================================================"
    echo ""
    docker run --net=host -v "$PWD"/"$modelIdentifier"/contrib_src:/contrib_src "$dockerIdentifier"
}

function runExpert()
{
    echo ""
    echo "============================================================"
    echo "Modelhub Docker started in expert mode."
    echo "Open the link displayed below to show jupyter dashboard and"
    echo "open sandbox.ipynb for a prepared playground."
    echo "Press CTRL+C to quit session."
    echo "============================================================"
    echo ""
    docker run --net=host -v "$PWD"/"$modelIdentifier"/contrib_src:/contrib_src "$dockerIdentifier" jupyter notebook --allow-root
}

function runBash()
{
    echo ""
    echo "============================================================"
    echo "Modelhub Docker started in interactive bash mode."
    echo "You can freely explore the docker here."
    echo "Press CTRL+D to quit session."
    echo "============================================================"
    echo ""
    docker run -it --net=host -v "$PWD"/"$modelIdentifier"/contrib_src:/contrib_src "$dockerIdentifier" /bin/bash
}

if [ "$MODE" = "basic" ]; then
    runBasic
elif [ "$MODE" = "expert" ]; then
    runExpert
elif [ "$MODE" = "bash" ]; then
    runBash
fi
