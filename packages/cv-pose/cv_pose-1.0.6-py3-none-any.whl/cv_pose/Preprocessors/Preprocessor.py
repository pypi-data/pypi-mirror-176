# This is a wrapper around the functions that will be passed into map
import warnings

class Preprocessor:
    def getMap(self, *args):
        warnings.warn('WARNING: The getMap() function in class `{className}` has not been implemented.'.format(className = self.__class__))