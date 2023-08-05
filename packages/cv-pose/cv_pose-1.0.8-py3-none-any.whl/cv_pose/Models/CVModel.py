# This is a wrapper around the Tensorflow.Model class. Here we can just add some meta data to keep things tidy
# I'm not implementing this yet because I think we won't be needing it. But I wanted this file here as
# a reminder.
import warnings

class CVModel:
    def getModel(self, *args):
        warnings.warn('WARNING: The getModel() function in class `{className}` has not been implemented.'.format(className = self.__class__))
        pass