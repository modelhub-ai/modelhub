import onnx
import caffe2.python.onnx.backend
import json
from processing import ImageProcessor
from modelhublib.model import ModelBase


class Model(ModelBase):

    def __init__(self):
        # load config file
        config = json.load(open("model/config.json"))
        # get the image processor
        self._imageProcessor = ImageProcessor(config)
        # load the DL model
        self._model = onnx.load('model/model.onnx')
    

    def infer(self, input):
        # load preprocessed input
        inputAsNpArr = self._imageProcessor.loadAndPreprocess(input)
        # Run inference with caffe2
        results = caffe2.python.onnx.backend.run_model(self._model, [inputAsNpArr])
        # postprocess results into output
        output = self._imageProcessor.computeOutput(results)
        return output
        

