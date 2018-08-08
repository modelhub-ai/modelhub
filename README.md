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

   Download [_start.py_](https://raw.githubusercontent.com/modelhub-ai/modelhub/master/start.py) 
   (right click -> "save link as") from this repository and place it into an empty folder.
   
4. **Run a model using start.py**

   Open a terminal and navigate to the folder that contains _start.py_. For running models, write access 
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

**_HINT_** Take a look at an already integrated model to understand how it looks when finished ([AlexNet](https://github.com/modelhub-ai/AlexNet) is a good and simple example).

1. **Prepare Docker image**

   1. Write a dockerfile preparing/installing all third party dependencies your model needs 
      (e.g. the deep learning library you are using). Use the `ubuntu:16.04` Docker image as base.
      
      You can check out examples of environments that we prepared 
      [here](https://github.com/modelhub-ai/modelhub-engine/tree/master/docker).
   
   2. Build your docker image.
   
   3. Adapt the [_Dockerfile_modelhub_](https://github.com/modelhub-ai/modelhub-engine/blob/master/Dockerfile_modelhub) 
      located in the modelhub-engine repository to use your docker image as base (change the first line in the file).
      
   4. Build the image from the modified Dockerfile_modelhub. This will include the modelhub engine into your docker.
   
   5. Push the image from the previous step to [DockerHub](https://hub.docker.com/) 
      (required if you want to publish your model on Modelhub, so the image can 
      be found when starting a model for the first time. If you don't plan to publish on Modelhub, this step is optional).
   
   -  **_NOTE_** We are planning to provide a few pre-build Docker images for the most common deep learning 
      frameworks, so you do not have to build them yourself. For now what we have is not really consolidated yet.
      Nevertheless, you can check out the Docker install scripts we are using 
      [here](https://github.com/modelhub-ai/modelhub-engine/tree/master/docker), they also serve as examples to 
      prepare your own. You can also try any of the existing 
      [pre-build images on DockerHub](https://hub.docker.com/u/modelhub/) - use the ones that start with _modelhub/main__.
      
2. **Prepare your model based on the modelhub template**

   1. Fork the model template https://github.com/modelhub-ai/model-template.git.
   
   2. Change the name of your model-template fork to your model's name. For this open your fork on GitHub, 
      go to _Settings_, change the _Repository name_, and press _Rename_.
      
   3. Clone your renamed fork to your local computer.
   
   4. Populate the configuration file _contrib_src/model/config.json_ with the relevant information about your model. 
      Please refer to the [schema](https://github.com/modelhub-ai/modelhub/blob/master/config_schema.json) for 
      allowed values and structure.
   
   5. Place your pre-trained model file(s) into the _contrib_src/model/_ folder.
   
   6. (optional) Place some sample data into the _contrib_src/sample_data/_ folder. This is not mandatory
      but highly recommended, so users can try your model directly.
   
   7. Open _contrib_src/inference.py_ and replace the model initialization and inference with your 
      model specific code. The template example shows how to integrate models in ONNX format and running
      them in caffe2. If your are using a different model format and/or backend you have to change this.
      
      There are only two lines you have to modify. In the `__init__` function change the following line,
      which loads the model:
      ```python
      # load the DL model (change this if you are not using ONNX)
      self._model = onnx.load('model/model.onnx')
      ```
      In the `infer` function change the following line, which runs the model prediction on the input data:
      ```python
      # Run inference with caffe2 (change this if you are using a different DL framework)
      results = caffe2.python.onnx.backend.run_model(self._model, [inputAsNpArr])
      ```
      
      **Note** Feel free to add functions to the _Model_ class as needed to structure your model's initialization 
      and execution code. But make sure to keep the pre- and post-processing of the input data and prediction 
      results (done by the _ImageProcessor_) as they are. In the next step you will implement the _ImageProcessor_.
   
   8. Open _contrib_src/processing.py_ to implement the _ImageProcessor_ class. The _ImageProcessor_ inherits
      from _ImageProcessorBase_, which already has most of the required data I/O processing implemented. Just your model
      specific pre- and post-processing has to be implemented, to make the _ImageProcessor_ work. There are two 
      pre-processing functions and one post-processing function to be filled in. We'll go through each of these 
      functions individually:
      
      1. **_preprocessBeforeConversionToNumpy(self, image)**
      
         The _ImageProcessorBase_ takes care of loading the input image and then calls this function to let you
         perform pre-processing on the image. The image comming into this function is either a 
         [PIL](https://pillow.readthedocs.io/en/latest/) or a [SimpleITK](http://www.simpleitk.org/) object.
         So this __preprocessBeforeConversionToNumpy_ gives you the option to perform pre-processing using PIL
         or SimpleITK, which might be more convenient than performing pre-processing on the image in numpy format
         (see next step). If you decide to implement pre-porcessing here, you should implement it for both, PIL and 
         SimpleITK objects. Make sure this function returns the same type of object as it received (PIL in => PIL out, 
         SimpleITK in => SimpleITK out).
         
         You do not have to implement this, alternatively you can just pass the image through unaltered and perform
         all your pre-processing using the image converted to numpy (see next step).
      
      2. **_preprocessAfterConversionToNumpy(self, npArr)**
      
         After the image has passed through the previous function, it is automatically converted to a numpy array 
         and then passed into this function. Here you must implement all additional pre-processing and numpy re-formating 
         necessary for your model to perform inference on the numpy array. The numpy array returned by this function 
         should have the right input format for your model (the output of this function is exactly what is returned 
         by `self._imageProcessor.loadAndPreprocess(input)` in _contrib_src/inference.py_).
      
      3. **computeOutput(self, inferenceResults)**
      
         This function receives the direct output of your model's inference. Here you must implement all
         post-processing required to prepare the output in a format that is supported by Modelhub.
         
         You can either output a list of dictionaries, where each dictionary has a "label" element, giving the
         name of a class, and a "probability" element, giving the probability of that class. For example:
         ```python
         result = []
         for i in range (len(inferenceResults)):
             obj = {'label': 'Class ' + str(i),
                    'probability': float(inferenceResults[i])}
             result.append(obj)
         ```
         For this you have to specifiy output type "label_list" in your model's _config.json_.
         
         Or you can output a numpy array. The output type specified in model's _config.json_ will help
         users (and Modelhub) to interpret the meaning result array:
         
         | Type          | Description   |
         | ------------- | ------------- |
         | vector        | 1d            |
         | mask_image    | 2d or 3d, discrete values, 0 is always background, 1,2... are the regions       |
         | heatmap       | 2d grayscale, 2d multi, 3d grayscale, 3d multi, if normalized, 1 is highest, 0 is lowest       |
         | image         | 2d grayscale, 2d multi, 3d grayscale, 3d multi     |
         | custom        | none of the above     |
   
   9. Edit _init/init.json_ and add the id of your Docker, so when starting your model, Modelhub knows 
      which Docker to use (and download from DockerHub).
      
      Optionally also list any additional files that are hosted externally (i.e. not in your model's GitHub repository).
      Specify origin and the destination within your model's folder structure. This is particularly useful for 
      pre-trained model files, since they can easily be larger than the maximum file size allowed by GitHub.
      
      When starting a model, Modelhub will first download the model's repository, then download any external files, 
      and then start the Docker specified in this init file.
   
   10. Add your licenses for the model (i.e. everything in the repsoitory except the sample data) and the sample data to
       _contrib_src/license/model_ and _contrib_src/license/sample_data_ respectively.
   
   11. (optional) Customize example code in _contrib_src/sandbox.ipynb_. This jupyter notebook is supposed
       to showcase how to use your model and interpret the output from python. The standard example code in this 
       notebook is very basic and generic. Usually it is much more informative to a user of your model if the
       example code is tailored to your model.
       
       You can access and run the Sandbox notebook by starting your model via `python start.py YOUR_MODEL_FOLDER_NAME`. 
       For this, copy _start.py_ from the [modelhub repository](https://github.com/modelhub-ai/modelhub) to the 
       parent folder of your model folder.

3. **Run tests**

   1. Manually check if your model works. 
      
      1. Copy _start.py_ from the 
         [modelhub repository](https://github.com/modelhub-ai/modelhub) to the parent folder of your model folder.
      
      2. Run `python start.py YOUR_MODEL_FOLDER_NAME` and check if the wep app for your model looks and works as expected.
      
      3. Run `python start.py YOUR_MODEL_FOLDER_NAME -e` and check if the jupyter notebook _contrib_src/sandbox.ipynb_ 
         works as expected.
   
   2. Run automatic integration test. This test will perform a few sanity checks to verify that all the basics
      seem to be working properly. Passing this test does not mean your model performs correctly (hence the manual
      checks).
      
      1. Copy _test_integration.py_ from the 
         [modelhub repository](https://github.com/modelhub-ai/modelhub) to the parent folder of your model folder.
      
      2. Run `python test_integration.py YOUR_MODEL_FOLDER_NAME`. If all tests pass you are good to publish.
      
         On some platforms (Windows, Mac) communication to the model's Docker container might fail if the
         Docker is started implicitly by the integration test. If you get obscure errors during test, try
         starting your model in a different terminal and running the test with the "-m" option.
         
         If your model needs particularly long to start up, you need to tell the integration test how long
         to wait before attempting to communicate with the model. Use the "-t" option.
         
         Check out the documentation of the integration test by calling `python test_integration.py -h`      
      
4. **Publish**

   1. `git clone https://github.com/modelhub-ai/modelhub.git` (or update if you cloned already).
   
   2. Add your model to the model index list _models.json_.
   
   3. Send us a pull request.



## About Us: 
We are the [Computational Imaging and Bioinformatics Laboratory](http://www.cibl-harvard.org/) at the Harvard Medical School, Brigham and Women’s Hospital and Dana-Farber Cancer Institute. We are a data science lab focused on the development and application of novel Artificial Intelligence (AI) approaches to various types of medical data.
