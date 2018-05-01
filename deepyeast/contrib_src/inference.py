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
    # Run inference with caffe2
    results = caffe2.python.onnx.backend.run_model(model, [inputAsNpArr])
    # postprocess results into output
    postprocessor = Postprocessor(config_json)
    output = postprocessor.computeOutput(results)
    return output
