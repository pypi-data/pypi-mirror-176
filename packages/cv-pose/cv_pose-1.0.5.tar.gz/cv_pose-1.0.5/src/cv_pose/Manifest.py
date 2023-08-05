from Preprocessors.ExamplePreprocessor import ExamplePreproccesor
from Preprocessors.SoftGatedSkipConvBasicPreprocessor import SoftGatedSkipConvBasicPreprocessor
from Models.ExampleModel import ExampleModel
from Models.SoftSkipConv import SoftSkipConv
from Datasets.DatasetSpecs.MPII.MPIIDatasetSpecs import MPII
from Datasets.DatasetSpecs.MPII.ClimbingSplit import ClimbingSplit



# Elements of the form "ModelID": CVModel class
ModelIDs = {"ExampleModel": ExampleModel, "SoftSkipConv": SoftSkipConv}

# Elements of the form "PreprocessorID": Preprocessor class
PreprocessorIDs = {"ExamplePreproccesor": ExamplePreproccesor, "SoftGatedSkipConvBasicPreprocessor": SoftGatedSkipConvBasicPreprocessor}

# Elements of the form "DatasetSpecID": DatasetSpec class
DatasetSpecs = {"MPII": MPII, "MPII_ClimbingSplit":ClimbingSplit}
