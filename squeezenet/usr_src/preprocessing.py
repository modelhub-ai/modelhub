from modelhublib.preprocessor import ImagePreprocessorBase
import PIL
import SimpleITK
import numpy as np


class ImagePreprocessor(ImagePreprocessorBase):

    def _preprocessBeforeConversionToNumpy(self, image):
        if isinstance(image, PIL.Image.Image):
            image = image.resize((224,224), resample = PIL.Image.LANCZOS)
        elif isinstance(image, SimpleITK.Image):
            newSize = [224, 224]
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
        if npArr.shape[1] > 3:
            npArr = npArr[:,0:3,:,:]
        elif npArr.shape[1] < 3:
            npArr = npArr[:,[0],:,:]
            npArr = np.concatenate((npArr, npArr[:,[0],:,:]), axis = 1)
            npArr = np.concatenate((npArr, npArr[:,[0],:,:]), axis = 1)
        #npArr[:, (2, 1, 0), :, :]
        npArr = npArr - 127.5
        return npArr
