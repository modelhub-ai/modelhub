#!/bin/bash

declare -r dockerIdentifier="modelhub/main_caffe_jonlong:0.1.0"
declare -r commitId="master"
declare -r serverAddress="https://raw.githubusercontent.com/modelhub-ai/modelhub/""$commitId""/models/"
declare -r modelIdentifier="CascadedFCN_Liver"
declare -a -r requiredFiles=("$modelIdentifier""/contrib_src/inference.py"
                             "$modelIdentifier""/contrib_src/postprocessing.py"
                             "$modelIdentifier""/contrib_src/preprocessing.py"
                             "$modelIdentifier""/contrib_src/run.py"
                             "$modelIdentifier""/contrib_src/sandbox.ipynb"
                             "$modelIdentifier""/contrib_src/license/model"
                             "$modelIdentifier""/contrib_src/license/sample_data"
                             "$modelIdentifier""/contrib_src/model/config.json"
                             "$modelIdentifier""/contrib_src/model/step1/README.md"
                             "$modelIdentifier""/contrib_src/model/step1/step1_deploy.prototxt"
                             "$modelIdentifier""/contrib_src/model/step2/README.md"
                             "$modelIdentifier""/contrib_src/model/step2/step2_deploy.prototxt"
                             "$modelIdentifier""/contrib_src/sample_data/3Dircadb1.1_image_70.png"
                             "$modelIdentifier""/contrib_src/sample_data/3Dircadb1.5_image_80.png"
                             "$modelIdentifier""/contrib_src/sample_data/3Dircadb1.10_image_60.png"
                             "$modelIdentifier""/contrib_src/sample_data/3Dircadb1.15_image_75.png"
                             "$modelIdentifier""/contrib_src/sample_data/3Dircadb1.17_image_90.png"
                             "$modelIdentifier""/contrib_src/sample_data/3Dircadb1.20_image_150.png"
                             "$modelIdentifier""/contrib_src/sample_data/dicom/3Dircadb1.1_image_70"
                             "$modelIdentifier""/contrib_src/sample_data/dicom/3Dircadb1.5_image_80"
                             "$modelIdentifier""/contrib_src/sample_data/dicom/3Dircadb1.10_image_60"
                             "$modelIdentifier""/contrib_src/sample_data/dicom/3Dircadb1.15_image_75"
                             "$modelIdentifier""/contrib_src/sample_data/dicom/3Dircadb1.17_image_90"
                             "$modelIdentifier""/contrib_src/sample_data/dicom/3Dircadb1.20_image_150"
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
    # trying to get model data with wget
    echo "$modelIdentifier model data folder does not exist yet."
    if command -v wget >/dev/null 2>&1; then
        echo "Getting model data with wget"
        for file in "${requiredFiles[@]}"
        do
          mkdir -p $(dirname "$file")
          wget -O "$file" "$serverAddress""$file"
        done
        # custom extra stuff: getting the weights from a different location
        wget -O "$modelIdentifier""/contrib_src/model/model.caffemodel" https://www.dropbox.com/s/aoykiiuu669igxa/step1_weights.caffemodel?dl=1
        wget -O "$modelIdentifier""/contrib_src/model/step1/step1_weights.caffemodel" https://www.dropbox.com/s/aoykiiuu669igxa/step1_weights.caffemodel?dl=1
        wget -O "$modelIdentifier""/contrib_src/model/step2/step2_weights.caffemodel" https://www.dropbox.com/s/ql10c37d7ura23l/step2_weights.caffemodel?dl=1
    else
        echo >&2 "Wget is required to download the model data from modelhub. Please install either of them and run this script again."
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
