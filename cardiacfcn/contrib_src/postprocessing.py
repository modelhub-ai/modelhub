from modelhublib.postprocessor import PostprocessorBase
from PIL import Image

class Postprocessor(PostprocessorBase):

    def computeOutput(self, inferenceResults):

        # get rid of 1's in the input
        inferenceResults=inferenceResults.reshape(200,200)

        # convert to image
        im = Image.fromarray((inferenceResults*255).astype('uint8'), 'L')

        print ('postprocessing done.')
        return im
