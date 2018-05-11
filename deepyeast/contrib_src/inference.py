import onnx
import caffe2.python.onnx.backend
import numpy as np
import json
from preprocessing import ImagePreprocessor
from postprocessing import Postprocessor

def infer(input):
    config_json = json.load(open("model/config.json"))
    # load preprocessed input
    preprocessor = ImagePreprocessor(config_json)
    inputAsNpArr = preprocessor.load(input)
    # load ONNX model
    model = onnx.load('model/model.onnx')
    # Check the model
    onnx.checker.check_model(model)
    print('The model is checked!')
    print inputAsNpArr
    print inputAsNpArr.shape
    # Run inference with caffe2
    results = caffe2.python.onnx.backend.run_model(model, [inputAsNpArr])
    print "inference run"
    # postprocess results into output
    # print config_json
    postprocessor = Postprocessor(config_json)
    # print postprocessor
    output = postprocessor.computeOutput(results)
    # print output
    return output
