#may take parameters, here it takes none
from Preprocessors.Preprocessor import Preprocessor
import numpy as np
import tensorflow as tf
import warnings

class OcclusionPreprocessor(Preprocessor):
    def getMap():
        def occlude_joints(im, j, wt, c, s):
            rng = tf.random.Generator.from_seed(1)
            indices_shuffled = tf.random.shuffle(tf.where(wt==1))[:,0]
            min_box_half_size, max_box_half_size, max_occlusions = 20, 30, len(indices_shuffled) + 1
            num_to_occlude = rng.uniform(shape=[], minval=0, maxval=max_occlusions, dtype=tf.int32)
            patch_half_width = rng.uniform(shape=[], minval=min_box_half_size, maxval=max_box_half_size, dtype=tf.int32)
            im_n = im.numpy()
            shape_x, shape_y = tf.cast(im_n.shape[1], tf.int32), tf.cast(im_n.shape[0], tf.int32)
            for i in range(num_to_occlude):
                index_to_occlude = indices_shuffled[i]
                x, y = tf.cast(j[index_to_occlude,0], tf.int32), tf.cast(j[index_to_occlude,1], tf.int32)
                min_y, max_y = max(y - patch_half_width, 0), min(y + patch_half_width + 1, shape_y)
                min_x, max_x = max(x - patch_half_width, 0), min(x + patch_half_width + 1, shape_x)
                im_n[min_y: max_y, min_x: max_x, :] = _get_background_patch(im, max_x - min_x, max_y - min_y)
                wt = tf.tensor_scatter_nd_update(wt, [[index_to_occlude]], [0])
            return im_n, j, wt
        # function which gets a patch of size height x width to occlude the image with 
        def _get_background_patch(im, width, height):
            return im[0:height, 0: width,:]
        def occlusion_wrapper(i, j, wt, loc):
            c = loc[0:2]
            s = loc[2]
            im, j, wt =  tf.py_function(occlude_joints, [i, j, wt, c, s], [tf.float32, tf.float32, tf.float32])
            im.set_shape(i.get_shape())
            return im, j, wt, loc
        return occlusion_wrapper