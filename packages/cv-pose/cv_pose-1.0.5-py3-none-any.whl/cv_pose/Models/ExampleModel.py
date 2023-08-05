import tensorflow as tf
from tensorflow import keras
from keras import layers

from Models.CVModel import CVModel

#may take parameters, here it takes none
class ExampleModel(CVModel):
    def getExampleModel(self):
        model = keras.Sequential(
            [
                layers.Dense(2, activation="relu", name="layer1"),
                layers.Dense(3, activation="relu", name="layer2"),
                layers.Dense(4, name="layer3"),
            ]
        )
        x = tf.ones((3, 3))
        y = model(x)
        return y