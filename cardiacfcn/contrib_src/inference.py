import keras
import numpy as np
import json
from preprocessing import ImagePreprocessor
from postprocessing import Postprocessor
from fcn_model import fcn_model
import keras.backend as K


def infer(input):
    config_json = json.load(open("model/config.json"))
    K.tensorflow_backend.clear_session()

    # load preprocessed input
    preprocessor = ImagePreprocessor(config_json)
    inputAsNpArr = preprocessor.load(input)

    # load keras architecture and weights
    model = fcn_model((200, 200, 1), 2, weights=None)
    model.load_weights("model/weights.h5")

    # Run inference
    results = model.predict(inputAsNpArr)

    # convert to image through postprocessing
    postprocessor = Postprocessor(config_json)
    output = postprocessor.computeOutput(results)

    # resize the image to inputSize - temporary step (to be moved)
    output = preprocessor._resizeToInputSize(output)

    # clear the computational graph
    K.tensorflow_backend.clear_session()
    return output
