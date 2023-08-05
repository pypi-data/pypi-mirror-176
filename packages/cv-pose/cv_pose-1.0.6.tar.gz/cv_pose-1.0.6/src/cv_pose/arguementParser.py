import tensorflow as tf
import Manifest
import pandas as pd 
import numpy as np

# the same thing in concept to getPreProcessor, returns tensorflow model
# every model will have an assocossiated ID, returns a tensorflow.model object 
def getModel(modelName: str):
    if (modelName not in Manifest.ModelIDs.keys()):
        raise KeyError
    cvModel = Manifest.ModelIDs[modelName]
    return cvModel.getModel()

# (csv location, folderOfImages location)
def getDataset(csvLocation: str, imagesLocation: str, datasetSpecName: str):
    df = pd.read_csv(csvLocation)
    imageNames = np.array([row[1].tolist()[0] for row in df.iterrows()])
    imageLabels = np.array([row[1].tolist()[1:] for row in df.iterrows()])
    datasetSpec = getDatasetSpec(datasetSpecName=datasetSpecName)
    dataset = tf.data.Dataset.from_tensor_slices((imageNames, imageLabels))
    #datasetSpec = getDatasetSpec(datasetSpecName)("","","")
    #image_label_pairs = np.array([datasetSpec.get_components(row[1].tolist()) for row in df.iterrows()])

    #imagesNames = image_label_pairs[:,0].tolist()
    #imageLabels = image_label_pairs[:,1].tolist()
    #raggedBoi = tf.ragged.constant((imagesNames, imageLabels))
    #ds_train = tf.data.Dataset.from_tensor_slices((imagesNames, imageLabels))
    def string_length_tf(t):
        return tf.py_function(len, [t], [tf.int64])
    def parse_image(filename, label):
        image_path = imagesLocation+"/"+filename
    #     image = tf.io.read_file(imagesLocation+"/"+filename)
    #    # try:
    #    #     # keep in mind that this assumes mac file system
    #    #     image = tf.io.read_file(imagesLocation+filename)
    #    # except:
    #    #     return np.zeros((10)), label
    #     image = tf.image.decode_image(image, channels=1, dtype=tf.float32)
    #     image.set_shape(image.get_shape())
    #     return image, label
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

# ds (dataset object)(tensorflow dataset)
# ds.map(function)
def getPreProcessor(preprocessorName: str):
    if (preprocessorName not in Manifest.PreprocessorIDs.keys()):
        raise KeyError
    preprocessor = Manifest.PreprocessorIDs[preprocessorName]
    return preprocessor.getMap()

def getDatasetSpec(datasetSpecName: str):
    if (datasetSpecName not in Manifest.DatasetSpecs.keys()):
        raise KeyError
    datasetSpec = Manifest.DatasetSpecs[datasetSpecName]
    return datasetSpec