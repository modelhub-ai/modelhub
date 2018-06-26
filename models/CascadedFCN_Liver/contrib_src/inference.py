import caffe
caffe.set_mode_cpu()
import json
import os
from processing import ImageProcessor
from modelhublib.model import ModelBase


class Model(ModelBase):

    def __init__(self):
        # load config file
        config = json.load(open("model/config.json"))
        # get the image processor
        self._imageProcessor = ImageProcessor(config)
        # load the DL model
        self._model = caffe.Net("model/step1/step1_deploy.prototxt", 
                                "model/step1/step1_weights.caffemodel", 
                                caffe.TEST)
    

    def infer(self, input):
        # load preprocessed input
        inputAsNpArr = self._imageProcessor.loadAndPreprocess(self._getDicomFilename(input))
        # Run inference
        self._model.blobs['data'].data[...] = inputAsNpArr
        results = self._model.forward()
        # postprocess results into output
        output = self._imageProcessor.computeOutput(results)
        return output


    def _getDicomFilename(self, inputFilename):
        path, filename = os.path.split(inputFilename)
        filename, _ = os.path.splitext(filename)
        dicomFilename = str(os.path.join(path, "dicom", filename))
        return dicomFilename


