from modelhublib.preprocessor import ImagePreprocessorBase
import PIL
import SimpleITK
import numpy as np


class ImagePreprocessor(ImagePreprocessorBase):

    def _preprocessBeforeConversionToNumpy(self, image):
        if isinstance(image, PIL.Image.Image):
            image = image.resize((64,64), resample = PIL.Image.LANCZOS)
        else:
            raise IOError("Image Type not supported for preprocessing.")
        return image

    def _preprocessAfterConversionToNumpy(self, npArr):
        print npArr.shape
        #if npArr.shape[1] > 3:
        npArr = npArr[:,0:2,:,:]
        # elif npArr.shape[1] < 3:
        #     npArr = npArr[:,[0],:,:]
        #     npArr = np.concatenate((npArr, npArr[:,[0],:,:]), axis = 1)
        #     npArr = np.concatenate((npArr, npArr[:,[0],:,:]), axis = 1)
        #npArr[:, (2, 1, 0), :, :]
        #npArr = npArr - 127.5
        npArr /= 255.
        npArr -= 0.5
        npArr *= 2.
        print npArr.shape
        return npArr
