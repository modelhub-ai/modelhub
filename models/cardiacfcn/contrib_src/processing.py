from modelhublib.processor import ImageProcessorBase
import PIL
import SimpleITK
import numpy as np
import json


class ImageProcessor(ImageProcessorBase):
        
    def _preprocessBeforeConversionToNumpy(self, image):
        if isinstance(image, PIL.Image.Image):
            self.inputSize = image.size
            image = image.resize((200,200), resample = PIL.Image.LANCZOS)
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


    def _preprocessAfterConversionToNumpy(self, npArr):
        # if has multiple chanels, take the first
        if npArr.shape[1] > 1:
            npArr = npArr[:,0:1,:,:]
        return npArr.reshape(1,npArr.shape[2],npArr.shape[3],1)


    def computeOutput(self, inferenceResults):
        # get rid of 1's in the input
        inferenceResults=inferenceResults.reshape(200,200)
        # convert to 4 channels
        inferenceResults = self._toRgba(inferenceResults)
        image = PIL.Image.fromarray(inferenceResults, 'RGBA')
        # reasmple back to original input size
        image = image.resize((self.inputSize[0],self.inputSize[1]), resample = PIL.Image.LANCZOS)
        print ('postprocessing done.')
        return image


    def _toRgba(self, arr):
        # convert to 255 uint8
        arr = (arr*255).astype('uint8')
        alpha = np.full((arr.shape), 255)
        return np.asarray(np.dstack((arr, arr, arr, alpha)), dtype=np.uint8)


