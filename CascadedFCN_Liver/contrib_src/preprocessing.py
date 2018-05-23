from modelhublib.preprocessor import ImagePreprocessorBase
import PIL
import SimpleITK
import numpy as np
import scipy
import scipy.misc


class ImagePreprocessor(ImagePreprocessorBase):

    def _preprocessBeforeConversionToNumpy(self, image):
        if isinstance(image, PIL.Image.Image):
            # OPTIONAL TODO: implement preprocessing of PIL image objects
            pass
        elif isinstance(image, SimpleITK.Image):
            # OPTIONAL TODO: implement preprocessing of SimpleITK image objects
            pass
        else:
            raise IOError("Image Type not supported for preprocessing.")
        return image


    def _preprocessAfterConversionToNumpy(self, npArr):
        npArr = np.squeeze(npArr)
        self.inputSize = npArr.shape
        npArr = npArr.astype(np.float)
        npArr[npArr>1200] = 0
        npArr = np.clip(npArr, -100, 400)    
        npArr = self._normalize(npArr)
        npArr = self._rescale(npArr, (388,388))
        npArr = np.pad(npArr,((92,92),(92,92)), mode='reflect')
        npArr = npArr[np.newaxis, np.newaxis, ...]
        return npArr
    
    
    def _rescale(self, img, shape=None):
        height, width = shape
        max_ = np.max(img)
        factor = 255.0/max_ if max_ != 0 else 1
        return (scipy.misc.imresize(img,(height,width),interp="nearest")/factor).astype(np.float)


    def _normalize(self, img):
        """ Normalize image values to [0,1] """
        min_, max_ = float(np.min(img)), float(np.max(img))
        return (img - min_) / (max_ - min_)


    # temporary function - to be cleaned and moved to postprocessing
    def _resizeToInputSize(self, image):
        return image.resize((self.inputSize[1],self.inputSize[0]), resample = PIL.Image.NEAREST)
