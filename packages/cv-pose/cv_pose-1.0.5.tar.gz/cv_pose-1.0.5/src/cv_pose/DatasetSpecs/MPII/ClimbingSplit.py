from Datasets.DatasetSpecs.MPII.MPIIDatasetSpecs import MPII

class ClimbingSplit(MPII):
    def generate_csv(self):
        data_file_location = self.dataset_dir + "/mpii_human_pose_v1_u12_1.mat"
        MPII_DF = self._mat_to_pandas(data_file_location)
        MPII_climbing_df = MPII_DF[MPII_DF['activity'] == "rock climbing"]
        MPII_non_climbing_df = MPII_DF[MPII_DF['activity'] != "rock climbing"]
        MPII_climbing_df.to_csv(self.dataset_dir + "/" + "CLIMBING_ONLY" + self.csv_name, index=False)
        MPII_non_climbing_df.to_csv(self.dataset_dir + "/" + "NON_CLIMBING_ONLY" + self.csv_name, index=False)