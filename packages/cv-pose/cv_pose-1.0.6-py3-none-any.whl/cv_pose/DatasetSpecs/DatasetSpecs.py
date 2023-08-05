# this is a metadata class designed to help us handle inconsistencies between different pose databases 
# motivating example can be found here https://github.com/eldar/pose-tensorflow/blob/master/dataset/mpii.py
import warnings

class DatasetSpecs:
    def __init__(self, dataset_dir, images_folder, csv_name):
        # Relevant fields for training
        self.all_joints = []
        self.all_joints_names = []
        self.num_joints = 0

        #Relevant fields for file managment
        self.dataset_dir = ""
        self.images_folder = ""
        self.csv_name = ""

        warnings.warn("WARNING: Init function is not specified for the class {className}".format(className = self.__class__))
    
    # Returns the (image, label) pair under standard format
    def get_components(self, list_of_raw_elements):
        warnings.warn("WARNING: get_components function is not specified for the class {className}".format(className = self.__class__))
    
    # Download the images associated with this dataset
    def download_images(self):
        warnings.warn("WARNING: download_images function is not specified for the class {className}".format(className = self.__class__))
    
    # Download the file containing the labels for this dataset
    def download_data_file(self):
        warnings.warn("WARNING: download_data_file function is not specified for the class {className}".format(className = self.__class__))

    # Generates the test csv associated with this dataset in the specified directory. Data from csv is taken from dataFile
    def generate_csv(self):
        warnings.warn("WARNING: generate_csv function is not specified for the class {className}".format(className = self.__class__))