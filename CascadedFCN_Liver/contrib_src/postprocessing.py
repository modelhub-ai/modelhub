from modelhublib.postprocessor import PostprocessorBase
import PIL
import numpy as np

class Postprocessor(PostprocessorBase):

    def computeOutput(self, inferenceResults):
        inferenceResults = inferenceResults['prob'][0,1]
        # make sure the result dims are 2D
        inferenceResults=np.squeeze(inferenceResults)
        # create mask
        inferenceResults[inferenceResults < 0.5] = 0
        inferenceResults[inferenceResults >= 0.5] = 1
        # convert to 4 channels
        inferenceResults = self._to_rgba(inferenceResults)
        print inferenceResults.shape
        result = PIL.Image.fromarray(inferenceResults, 'RGBA')
        return result

    def _to_rgba(self, arr):
        # convert to 255 uint8
        arr = (arr*255).astype(np.uint8)
        alpha = np.full((arr.shape), 255, dtype=np.uint8)
        return np.asarray(np.dstack((arr, arr, arr, alpha)), dtype=np.uint8)
