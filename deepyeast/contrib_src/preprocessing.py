from modelhublib.preprocessor import ImagePreprocessorBase
import PIL
import SimpleITK
import numpy as np


class ImagePreprocessor(ImagePreprocessorBase):

    def _preprocessBeforeConversionToNumpy(self, image):
        if isinstance(image, PIL.Image.Image):
            # OPTIONAL TODO: implement preprocessing of PIL image objects
        elif isinstance(image, SimpleITK.Image):
            # OPTIONAL TODO: implement preprocessing of SimpleITK image objects
        else:
            raise IOError("Image Type not supported for preprocessing.")
        return image

    def _preprocessAfterConversionToNumpy(self, npArr):
        # TODO: implement preprocessing of image after it was converted to a numpy array
        return npArr
