from modelhublib.postprocessor import PostprocessorBase
from PIL import Image
import numpy as np

class Postprocessor(PostprocessorBase):

    def computeOutput(self, inferenceResults):
        # get rid of 1's in the input
        inferenceResults=inferenceResults.reshape(200,200)
        # convert to 4 channels
        inferenceResults = self.to_rgba(inferenceResults)
        im = Image.fromarray(inferenceResults, 'RGBA')
        print ('postprocessing done.')
        return im

    def to_rgba(self, arr):
        # convert to 255 uint8
        arr = (arr*255).astype('uint8')
        alpha = np.full((arr.shape), 255)
        return np.asarray(np.dstack((arr, arr, arr, alpha)), dtype=np.uint8)
