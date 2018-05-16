from modelhublib.preprocessor import ImagePreprocessorBase
from PIL import Image
import SimpleITK
import numpy as np

class ImagePreprocessor(ImagePreprocessorBase):

    def _preprocessBeforeConversionToNumpy(self, image):

        if isinstance(image, Image.Image):
            self.inputSize = image.size
            image = image.resize((200,200), resample = Image.LANCZOS)
        elif isinstance(image, SimpleITK.Image):
            newSize = [200, 200]
            referenceImage = SimpleITK.Image(newSize, image.GetPixelIDValue())
            referenceImage.SetOrigin(image.GetOrigin())
            referenceImage.SetDirection(image.GetDirection())
            referenceImage.SetSpacing([sz*spc/nsz for nsz,sz,spc in zip(newSize,
                                                                        image.GetSize(),
                                                                        image.GetSpacing())])
            image = SimpleITK.Resample(image, referenceImage)
        else:
            raise IOError("Image Type not supported for preprocessing.")
        return image

    # temporary function - to be cleaned and moved to postprocessing
    def _resizeToInputSize(self, image):
        return image.resize((self.inputSize[0],self.inputSize[1]), resample = Image.LANCZOS)

    def _preprocessAfterConversionToNumpy(self, npArr):
        # if has multiple chanels, take the first
        if npArr.shape[1] > 1:
            npArr = npArr[:,0:1,:,:]
        return npArr.reshape(1,npArr.shape[2],npArr.shape[3],1)
