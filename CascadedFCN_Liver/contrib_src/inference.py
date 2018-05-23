import caffe
caffe.set_mode_cpu()
import numpy as np
import json
import os
from preprocessing import ImagePreprocessor
from postprocessing import Postprocessor


model = None


def infer(input):
    global model

    config_json = json.load(open("model/config.json"))
    
    # load preprocessed input
    preprocessor = ImagePreprocessor(config_json)
    inputAsNpArr = preprocessor.load(getDicomFilename(input))
    
    # load model
    if model is None:
        model = caffe.Net("model/step1/step1_deploy.prototxt", 
                          "model/step1/step1_weights.caffemodel", 
                          caffe.TEST)
    
    # Run inference
    model.blobs['data'].data[...] = inputAsNpArr
    results = model.forward()
    #del model

    # postprocess results into output
    postprocessor = Postprocessor(config_json)
    output = postprocessor.computeOutput(results)
    
    return preprocessor._resizeToInputSize(output)


def getDicomFilename(inputFilename):
    path, filename = os.path.split(inputFilename)
    filename, _ = os.path.splitext(filename)
    dicomFilename = str(os.path.join(path, "dicom", filename))
    return dicomFilename


