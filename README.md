We are building a collection of deep learning models for medical data (and beyond). Check it out [here](http://www.modelhub.ai).

Crowdsourced through contributions by the scientific research community, modelhub is a repository of deep learning models pretrained for a wide variety of medical applications. Modelhub highlights recent trends in deep learning applications, enables transfer learning approaches and promotes reproducible science.

This repository is the index/registry of all models, and as such the point where all developments under [modelhub-ai](https://github.com/modelhub-ai) come together. Read on to learn how to use it and how to contribute your own models.

## Quick Start

The most accessible way to experience modelhub is [via modelhub.ai](http://www.modelhub.ai). There you can explore the model collection, try them online, and find instructions on how to run models locally.

But since you are here, follow these steps to get modelhub running on your local computer:

1. **Install Docker** (if not already installed)
   
   Follow the [official Docker instrcutions](https://docs.docker.com/install/) to install Docker CE.
   Docker is required to run models.

2. **Install Python 2.7 or 3.6 (or higher)** (if not already installed)

   Download and install Python from the official [Python page](https://www.python.org/). Modelhub requires 
   Python 2.7 or Python 3.6 (or above).
   
3. **Downlad modelhub start script**

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
   the "-e" option, e.g. `python start.py SqueezeNet -e`. Follow the instructions on the temrinal to open the notebook.
   
   See additional starting options by executing `python start.py -h`.

Since you found modelhub on GitHub, you are probably (hopefully) also interested in contributing models to modelhub.ai and the framework we provide. Please read on ...

## Overview

<img width="500" alt="modelhub framework overview" src="https://raw.githubusercontent.com/modelhub-ai/modelhub/master/docs/images/framework_overview.png">

## Contribute Your Model to modelhub.ai

<img width="500" alt="modelhub contribution steps" src="https://raw.githubusercontent.com/modelhub-ai/modelhub/master/docs/images/contribution_process.png">

## About Us: 
We are the [Computational Imaging and Bioinformatics Laboratory](http://www.cibl-harvard.org/) at the Harvard Medical School, Brigham and Women’s Hospital and Dana-Farber Cancer Institute. We are a data science lab focused on the development and application of novel Artificial Intelligence (AI) approaches to various types of medical data.
