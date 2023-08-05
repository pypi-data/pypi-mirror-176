

#may take parameters, here it takes none
from Preprocessors.Preprocessor import Preprocessor
import warnings

class ExamplePreproccesor(Preprocessor):
    def getMap(self):
        warnings.warn('WARNING: The getMap() function in class `{className}` has not been implemented.'.format(className = self.__class__))
        pass