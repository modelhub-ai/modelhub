We are building a collection of deep learning models for medical data (and beyond). Check it out [here](http://www.modelhub.ai).

Crowdsourced through contributions by the scientific research community, modelhub is a repository of deep learning models pretrained for a wide variety of medical applications. Modelhub highlights recent trends in deep learning applications, enables transfer learning approaches and promotes reproducible science.

This repository is the index/registry of all models, and as such the point where all developments under [modelhub-ai](https://github.com/modelhub-ai) come together. Read on to learn how to use it and how to contribute your own models.


## Quick Start

The most accessible way to experience modelhub is via [modelhub.ai](http://www.modelhub.ai). There you can explore the model collection, try them online, and find instructions on how to run models locally.

But since you are here, follow these steps to get modelhub running on your local computer:

1. **Install Docker** (if not already installed)
   
   Follow the [official Docker instrcutions](https://docs.docker.com/install/) to install Docker CE.
   Docker is required to run models.

2. **Install Python 2.7 or 3.6 (or higher)** (if not already installed)

   Download and install Python from the [official Python page](https://www.python.org/). Modelhub requires 
   Python 2.7 or Python 3.6 (or higher).
   
3. **Download modelhub start script**

   Download [start.py](https://raw.githubusercontent.com/modelhub-ai/modelhub/master/start.py) (use "save link as") 
   from this repository and place it into an empty folder.
   
4. **Run a model using start.py**

   Open a terminal and navigate to the folder that contains start.py. For running models, write access 
   is required in the current folder.   
   
   Execute `python start.py SqueezeNet` in the terminal to run the SqueezeNet model from the modelhub collection. 
   This will download all required model files (only if they do not exist yet) and start the model. Follow the 
   instructions given on the terminal to access the web interface to explore the model.
   
   Replace `SqueezeNet` by any other model name in the collection to start a different model. To see a list of
   all available models execute `python start.py -l`.
   
   You can also access a jupyter notebook that allows you to experiment with a model by starting a model with 
   the "-e" option, e.g. `python start.py SqueezeNet -e`. Follow the instructions on the terminal to open the notebook.
   
   See additional starting options by executing `python start.py -h`.

Since you found modelhub on GitHub, you are probably also interested in packaging your own model with our framework and hopefully contributing it to Modelhub. Please read on ...


## Overview

Modelhub provides a framework into which contributors can plug-in their model and model specific code pre- and post-processing code. The framework provides a standalone runtime environment, convience functionality (e.g. image loading and conversion), programming interfaces to access the model, and a user friendly web-interface to try a model. See the following figure for an overview of the architecture.

<img width="500" alt="modelhub framework overview" src="https://raw.githubusercontent.com/modelhub-ai/modelhub/master/docs/images/framework_overview.png">

The _contrib_src_ contains the model specific code and data, all other functionality is provided by the framework. The framework and model specific code run inside of a Docker container, which contains all runtime dependencies. The resulting package constitutes a standalone unit that can be easily deployed, executed on different platforms (Linux, Windows, Mac), and integrated into existing applications via the generic API.



## Contribute Your Model to Modelhub

To package a model with our framework you need to have the following **prerequisites** installed:
- Python 2.7 or Python 3.6 (or higher)
- [Docker](https://docs.docker.com/install/)
- Clone of the [modelhub-engine repository](https://github.com/modelhub-ai/modelhub-engine.git) (`git clone https://github.com/modelhub-ai/modelhub-engine.git`)

Packaging your model with our framework and eventually contributing it to the Modelhub collection requires the following steps (read further for details).

<img width="500" alt="modelhub contribution steps" src="https://raw.githubusercontent.com/modelhub-ai/modelhub/master/docs/images/contribution_process.png">

1. **Build Docker Image**

   1. Write a dockerfile preparing/installing all third party dependencies your model needs 
      (e.g. the deep learning library you are using). Use the `ubuntu:16.04` Docker image as base.
      
      You can check out examples of environments that we prepared 
      [here](https://github.com/modelhub-ai/modelhub-engine/tree/master/docker).
   
   2. Build your docker image.
   
   3. Adapt the [_Dockerfile_modelhub_](https://github.com/modelhub-ai/modelhub-engine/blob/master/Dockerfile_modelhub) 
      located in the modelhub-engine repository to use your docker image as base (change the first line in the file).
      
   4. Build the image from the modified Dockerfile_modelhub. This will include the modelhub engine into your docker.
   
   5. Push the image from the previous step to [DockerHub](https://hub.docker.com/) 
      (required if you want to publish your model on Modelhub, such that the image can 
      be found when starting a model for the first time. If you don't plan to publish on Modelhub, this step is optional).
      
2. **Populate Template**

   - Git fork the model template https://github.com/modelhub-ai/model-template.git
   - Change the name of the repo to your model's name (from the website)
   - Clone locally
   - Populate config.json with relevant information (need to refer to schema to fill it in)
   - Put your model + license
   - Put inference code
   - (optional but highly recommended) Put sample images + license
   - (optional) define preprocessing on native file input
   - (optional) define preprocessing on numpy array
   - (optional) define postprocessing on output
   - (optional) customize example code in sandbox.ipynb
   - Init file (point to docker image + (optional) external files

3. **Run Tests**

   - Run test_integration.py on your model folder
   - Manually check frontend and sandbox.ipynb

4. **Publish**

   1. `git clone https://github.com/modelhub-ai/modelhub.git` (or update if you cloned already).
   
   2. Add your model to the model index list _models.json_.
   
   3. Send us a pull request.



## About Us: 
We are the [Computational Imaging and Bioinformatics Laboratory](http://www.cibl-harvard.org/) at the Harvard Medical School, Brigham and Women’s Hospital and Dana-Farber Cancer Institute. We are a data science lab focused on the development and application of novel Artificial Intelligence (AI) approaches to various types of medical data.
