import numpy as np
import scipy.io as sio
import pandas as pd
from cv_pose.DatasetSpecs.DatasetSpecs import DatasetSpecs
#import wget
import warnings

# This dataset represents the MPII dataset with all it's images and labels
class MPII(DatasetSpecs):
    def __init__(self, dataset_dir, images_folder, csv_name):
        self.all_joints = [[0, 5], [1, 4], [2, 3], [6, 11], [7, 10], [8, 9], [12], [13]]
        self.all_joints_names = ['ankle', 'knee', 'hip', 'wrist', 'elbow', 'shoulder', 'chin', 'forehead']
        self.num_joints = 14

        self.dataset_dir = dataset_dir
        self.images_folder = images_folder
        self.csv_name = csv_name

    def get_components(list_raw_elements):
        #file_name = list_raw_elements[0]
        joints = np.reshape(np.stack(list_raw_elements[0:32]), [16,2])
        weights = np.stack(list_raw_elements[32:48])
        loc = np.stack(list_raw_elements[48:51])
        return joints, weights, loc

    # TODO: finish this later
    def download_images(self):
        warnings.warn("WARNING: download_images function is not specified for the class {className}".format(className = self.__class__))
    
    # TODO: finish this later
    def download_data_file(self):
        warnings.warn("WARNING: download_data_file function is not specified for the class {className}".format(className = self.__class__))

    def _mat_to_pandas(self, mat_path: str, filter=True, print_progress=False):
        mat = sio.loadmat(mat_path, struct_as_record=False)
        rel = mat['RELEASE']
        obj_rel = rel[0,0]
        annolist = obj_rel.__dict__['annolist']
        
        # boolean array denoting which images are training vs testing: we are ignoring it for now...
        img_tra = obj_rel.__dict__['img_train']

        act = obj_rel.__dict__['act']

        data_arr = ['NAME','r_ankle_X', 'r_ankle_Y', 'r_knee_X', 'r_knee_Y', 'r_hip_X', 'r_hip_Y',
        'l_hip_X', 'l_hip_Y', 'l_knee_X', 'l_knee_Y', 'l_ankle_X', 'l_ankle_Y',
        'pelvis_X', 'pelvis_Y', 'thorax_X', 'thorax_Y', 'neck_X', 'neck_Y',
        'head_X', 'head_Y', 'r_wrist_X', 'r_wrist_Y', 'r_elbow_X', 'r_elbow_Y',
        'r_shoulder_X', 'r_shoulder_Y', 'l_shoulder_X', 'l_shoulder_Y', 'l_elbow_X',
        'l_elbow_Y', 'l_wrist_X', 'l_wrist_Y',
        'r_ankle_vis', 'r_knee_vis', 'r_hip_vis', 'l_hip_vis', 'l_knee_vis', 
        'l_ankle_vis', 'pelvis_vis', 'thorax_vis', 'neck_vis', 'head_vis',
        'r_wrist_vis', 'r_elbow_vis', 'r_shoulder_vis', 'l_shoulder_vis',
        'l_elbow_vis', 'l_wrist_vis', 'center_X', 'center_Y', 'scale','activity','category']

        data = pd.DataFrame(columns=data_arr)
        for ix in range(0, annolist.shape[1]):
            obj_list = annolist[0,ix]
            obj_act = act[ix,0]
            
            # get row joint annotations
            rect = obj_list.__dict__['annorect']
            # get image names
            img_d = obj_list.__dict__['image']
            if rect.shape[0] ==0:
                continue
            # iterate through each person in the image
            for i in range(rect.shape[1]):
                temp_arr = []
                obj_rect = rect[0,i]
                obj_img = img_d[0,0]
            
                if 'annopoints' not in obj_rect._fieldnames:
                    continue
                
                name_d = obj_img.__dict__['name']
                name = name_d[0]
                temp_arr.append(name)
                annopoints = obj_rect.__dict__['annopoints']
                if annopoints.shape[0]==0:
                    continue
                obj_points = annopoints[0,0]
                points = obj_points.__dict__['point']
                if filter:
                    if points.shape[1]!=16:
                        continue

                # get the points
                for n in range(0,32):
                    temp_arr.append(0)
                for px in range(0,points.shape[1]):
                    po = points[0,px]
                    po_id = po.__dict__['id']
                    po_x = po.__dict__['x']
                    po_y = po.__dict__['y']
                    ind = 2*po_id[0][0]+1
                    temp_arr[ind] = float(po_x[0][0])
                    temp_arr[ind+1] = float(po_y[0][0])
                
                # get the weights
                for n in range(0,16):
                    temp_arr.append(0)
                for px in range(0,points.shape[1]):
                    po = points[0,px]
                    po_id = po.__dict__['id']
                    ind = 33 + po.__dict__['id'][0][0]
                    po_vis = po.__dict__['is_visible']
                    if po_vis.shape == (0,0):
                        temp_arr[ind] = 0
                    else:
                        temp_arr[ind] = po_vis[0][0]
                    
                scale = obj_rect.__dict__['scale']
                obj_pos = obj_rect.__dict__['objpos']
                
                temp_arr.append((obj_pos[0][0].__dict__['x'][0][0]))
                temp_arr.append((obj_pos[0][0].__dict__['y'][0][0]))
                
                temp_arr.append(scale[0][0])
                
                # get context information
                activity = act[ix,0]
                a_n = activity.act_name
                c_n = activity.cat_name
                if a_n.shape[0]==0:
                    temp_arr.append(a_n)
                else:
                    temp_arr.append(activity.act_name[0])
                if c_n.shape[0]==0:
                    temp_arr.append(c_n)
                else:
                    temp_arr.append(activity.cat_name[0])

                arr = np.array(temp_arr)
                temp_data_f = pd.DataFrame([arr], columns=data_arr)
                data = pd.concat([data, temp_data_f]) 
            
            if print_progress and ix%100==0:
                print(ix)
        data = data[6:] 
        return data

    def generate_csv(self):
        data_file_location = self.dataset_dir + "/mpii_human_pose_v1_u12_1.mat"
        MPII_DF = self._mat_to_pandas(data_file_location)
        MPII_DF.to_csv(self.dataset_dir + self.csv_name, index=False)
        
