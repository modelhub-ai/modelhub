import keras
import json
from fcn_model import fcn_model
import keras.backend as K
from processing import ImageProcessor
from modelhublib.model import ModelBase


class Model(ModelBase):

    def __init__(self):
        # load config file
        config = json.load(open("model/config.json"))
        # get the image processor
        self._imageProcessor = ImageProcessor(config)
        # load the DL model
        self._model = fcn_model((200, 200, 1), 2, weights=None)
        self._model.load_weights("model/weights.h5")
        self._model._make_predict_function()


    def infer(self, input):
        # load preprocessed input
        inputAsNpArr = self._imageProcessor.loadAndPreprocess(input)
        # Run inference
        results = self._model.predict(inputAsNpArr)
        # postprocess results into output
        output = self._imageProcessor.computeOutput(results)
        return output


