import tensorflow as tf
from cv_pose.DatasetSpecs import DatasetSpecs
import pandas as pd 
import numpy as np

# (csv location, folderOfImages location)
def getDataset(csvLocation: str, imagesLocation: str, datasetSpec):
    df = pd.read_csv(csvLocation)
    imageNames = np.array([row[1].tolist()[0] for row in df.iterrows()])
    imageLabels = np.array([row[1].tolist()[1:] for row in df.iterrows()])
    dataset = tf.data.Dataset.from_tensor_slices((imageNames, imageLabels))

    def parse_image(filename, label):
        image_path = imagesLocation+"/"+filename
        path_length = tf.strings.length(image_path)
        file_extension = tf.strings.substr(image_path, path_length - 3, 3)
        file_cond = tf.equal(file_extension, 'jpg')
        
        image  = tf.cond(file_cond, lambda: tf.image.decode_jpeg(tf.io.read_file(image_path)), lambda: tf.image.decode_png(tf.io.read_file(image_path)))
        return tf.cast(image, tf.float32) / 256.0, label
    def get_elements_wrapper(image, label):
       j, w, loc =  tf.py_function(datasetSpec.get_components, [label], [tf.float32, tf.float32, tf.float32])
       return image, j, w, loc

    dataset = dataset.map(parse_image) 
    return dataset.map(get_elements_wrapper)
