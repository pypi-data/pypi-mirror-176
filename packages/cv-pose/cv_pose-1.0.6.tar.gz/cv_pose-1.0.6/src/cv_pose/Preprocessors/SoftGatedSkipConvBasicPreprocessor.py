import warnings
import tensorflow as tf
from tensorflow.keras.layers.experimental.preprocessing import Rescaling
import tensorflow_addons as tfa
import numpy as np
import matplotlib.pyplot as plt
from Preprocessors.Preprocessor import Preprocessor

class SoftGatedSkipConvBasicPreprocessor(Preprocessor):
    def getMap(image_size=256, heatmap_size=64, sigma=1):
        PI = 3.14159265
        NUM_JOINTS = 16
        mean = [0.4624228775501251, 0.44416481256484985, 0.4025438725948334]
        def _get_gaussian(coords):
            size = tf.constant(6. * sigma + 1.)
            x = tf.range(
                start=0., 
                limit=size, 
                delta=1,
            )
            y = tf.expand_dims(x, 1)
            x0 = y0 = tf.floor(size / 2)
            gaussian = tf.exp(
                - ((x - x0) ** 2 + (y - y0) ** 2) / (2 * sigma ** 2)
            )

            x_min = tf.maximum(0, -coords[0,0])
            x_max = tf.minimum(coords[1,0], heatmap_size) - coords[0,0]
            y_min = tf.maximum(0, -coords[0,1])
            y_max = tf.minimum(coords[1,1], heatmap_size) - coords[0,1]

            return gaussian[y_min:y_max, x_min:x_max]
        def _get_padding(coords):
            x_min = tf.maximum(0, coords[0,0])
            x_max = tf.minimum(coords[1,0], heatmap_size)
            y_min = tf.maximum(0, coords[0,1])
            y_max = tf.minimum(coords[1,1], heatmap_size)

            top = y_min if y_min != 0 else 0
            bottom = heatmap_size - y_max
            left = x_min if x_min != 0 else 0
            right = heatmap_size - x_max

            padding = tf.TensorArray(
                tf.int32, 
                size=2, 
                dynamic_size=False,
            )
            padding = padding.write(0, value=[top, bottom])
            padding = padding.write(1, value=[left, right])
            return padding.stack()
        def _draw_heatmap(joints):
            coords = tf.TensorArray(
                tf.int32, 
                size=2, 
                dynamic_size=False,
            )
            coords = coords.write(
                index=0, 
                value=[
                    tf.cast(joints[0] - 3 * sigma, tf.int32),
                    tf.cast(joints[1] - 3 * sigma, tf.int32),
                ],
            )
            coords = coords.write(
                index=1,
                value=[
                    tf.cast(joints[0] + 3 * sigma + 1, tf.int32),
                    tf.cast(joints[1] + 3 * sigma + 1, tf.int32,),
                ],
            )
            coords = coords.stack()
            if (
                coords[0,0] >= heatmap_size
                or coords[0,1] >= heatmap_size
                or coords[1,0] < 0
                or coords[1,1] < 0
            ):
                heatmap = tf.zeros([
                    heatmap_size, 
                    heatmap_size,
                ])
                visible = tf.zeros([])
                return heatmap, visible

            gaussian = _get_gaussian(coords)    
            padding = _get_padding(coords)
            heatmap = tf.pad(gaussian, padding)
            visible = tf.ones([])
            return heatmap, visible
        def _get_heatmap(joints, weights, center, scale, rotation):
            hm_size = tf.cast(heatmap_size, tf.float32)
            hm = tf.TensorArray(
                tf.float32, 
                size=NUM_JOINTS, 
                dynamic_size=False,
            )
            w = tf.TensorArray(
                tf.float32, 
                size=NUM_JOINTS, 
                dynamic_size=False,
            )
            for j in tf.range(NUM_JOINTS):
                if joints[j, 1] > 0:
                    joints_transformed = coord_transform(
                        joints[j,:] + 1, 
                        center, 
                        scale, 
                        rotation, 
                        tf.zeros([], tf.int32),
                        hm_size,
                    )
                    heatmap, visible = _draw_heatmap(joints_transformed - 1)
                    hm = hm.write(j, value=heatmap)
                    w = w.write(j, value=weights[j] * visible)
                else:
                    hm = hm.write(j, value=tf.zeros([hm_size, hm_size]))
                    w = w.write(j, value=weights[j])
            heatmap = tf.transpose(hm.stack(), perm=[1,2,0])
            weights = w.stack()
            return heatmap, weights
        def _crop_image(image, center, scale, rotation):
            ul_coords = coord_transform(
                tf.zeros([2]), 
                center, 
                scale, 
                rotation=tf.zeros([]),
                invert=tf.ones([], tf.int32),
                size=tf.cast(image_size, tf.float32),
            )
            br_coords = coord_transform(
                tf.cast(
                    [image_size, image_size], 
                    tf.float32,
                ), 
                center, 
                scale, 
                rotation=tf.zeros([]),
                invert=tf.ones([], tf.int32),
                size=tf.cast(image_size, tf.float32),
            )
            pad = tf.norm(
                tf.cast(br_coords - ul_coords, tf.float32)
            )
            pad = pad / 2
            pad = pad - tf.cast(br_coords[1] - ul_coords[1], tf.float32) / 2
            pad = tf.cast(pad, tf.int32)

            if rotation != 0.:
                ul_coords = ul_coords - pad
                br_coords = br_coords + pad

            x_min = tf.maximum(0, ul_coords[0])
            x_max = tf.minimum(tf.shape(image)[1], br_coords[0])
            y_min = tf.maximum(0, ul_coords[1])
            y_max = tf.minimum(tf.shape(image)[0], br_coords[1])
            x_min_margin = tf.maximum(0, -ul_coords[0])
            x_max_margin = (
                tf.minimum(br_coords[0], tf.shape(image)[1]) 
                - ul_coords[0]
            )
            y_min_margin = tf.maximum(0, -ul_coords[1]) 
            y_max_margin = (
                tf.minimum(br_coords[1], tf.shape(image)[0]) 
                - ul_coords[1]
            )
            
            if x_max_margin < x_min_margin:
                temp = x_max_margin
                x_max_margin = x_min_margin
                x_min_margin = temp
                temp = x_min
                x_min = x_max
                x_max = temp

            top = y_min_margin
            bottom = (br_coords[1] - ul_coords[1]) - y_max_margin
            left = x_min_margin
            right = (br_coords[0] - ul_coords[0]) - x_max_margin
                
            cropped_image = image[y_min:y_max, x_min:x_max]
            cropped_image = tf.pad(
                cropped_image, 
                paddings=[
                    [top, bottom], 
                    [left, right], 
                    [0, 0],
                ],
            )
            if rotation != 0.:
                cropped_image = tfa.image.rotate(
                    cropped_image, 
                    angles=rotation * (PI / 180),
                )
                cropped_image = cropped_image[pad:-pad, pad:-pad]
            return tf.image.resize(
                cropped_image, 
                size=[
                    image_size,
                    image_size,
                ],
            )
        def _get_cropped_image(image, center, scale, rotation):
            height = tf.cast(tf.shape(image)[0], tf.float32)
            width = tf.cast(tf.shape(image)[1], tf.float32)
            print(width)
            sf = scale * 200.0 / tf.cast(image_size, tf.float32)
            if sf < 2:
                return _crop_image(
                    image, 
                    center, 
                    scale, 
                    rotation,
                )
            else:
                max_size = tf.cast(
                    tf.floor(tf.maximum(height, width) / sf), 
                    tf.int32,
                )
                new_height = tf.cast(tf.floor(height / sf), tf.int32)
                new_width = tf.cast(tf.floor(width / sf), tf.int32)
                if max_size < 2:
                    return tf.zeros([
                        image_size, 
                        image_size, 
                        tf.shape(image)[2],
                    ])
                else:
                    image = tf.image.resize(image, size=[new_height, new_width])
                    center = center / sf
                    scale = scale / sf
                    return _crop_image(image, center, scale, rotation,)
        def coord_transform(
                coords, 
                center, 
                scale, 
                rotation, 
                invert,
                size,
            ):
            transfromation_matrix = get_transformation_matrix(
                center, 
                scale, 
                rotation, 
                invert, 
                size,
            )
            new_coords = tf.TensorArray(
                tf.float32, 
                size=3, 
                dynamic_size=False,
            )
            new_coords = new_coords.write(0, value=coords[0] - 1.)
            new_coords = new_coords.write(1, value=coords[1] - 1.)
            new_coords = new_coords.write(2, value=1.)
            new_coords = new_coords.stack()
            new_coords = tf.tensordot(
                transfromation_matrix, 
                new_coords,
                axes=1,
            )
            return tf.cast(new_coords[:2], tf.int32) + 1
        def get_transformation_matrix(
                center, 
                scale, 
                rotation, 
                invert, 
                size,
            ):
            transfromation_matrix = tf.TensorArray(
                tf.float32, 
                size=3, 
                dynamic_size=False,
            )
            transfromation_matrix = transfromation_matrix.write(
                index=0, 
                value=[
                    size / (scale * 200.), 
                    0., 
                    size * (-center[0] / (scale * 200.) + 0.5),
                ],
            )
            transfromation_matrix = transfromation_matrix.write(
                index=1, 
                value=[
                    0., 
                    size / (scale * 200.), 
                    size * (-center[1] / (scale * 200.) + 0.5),
                ],
            )
            transfromation_matrix = transfromation_matrix.write(2, value=[0., 0., 1.])
            transfromation_matrix = transfromation_matrix.stack()

            if rotation != 0.:
                transfromation_matrix = rotate_transformation_matrix(
                    transfromation_matrix,
                    rotation,
                    size,
                )
            if invert == 1:
                transfromation_matrix = tf.linalg.inv(transfromation_matrix)
            return transfromation_matrix
        def _generating_function(image, joints, weights, center,scale, rotation):
            image = _get_cropped_image(
                image, 
                center, 
                scale, 
                rotation,
            )
            heatmap, weights = _get_heatmap(
                joints, 
                weights, 
                center, 
                scale, 
                rotation,
            )
            image = tf.reshape(
                image, 
                shape=[
                    image_size, 
                    image_size, 
                    3,
                ],
            )     
            heatmap = tf.reshape(
                heatmap, 
                shape=[
                    heatmap_size,
                    heatmap_size,
                    NUM_JOINTS,
                ],
            )   
            return image, heatmap, weights
        def rotate_transformation_matrix(
                transfromation_matrix, 
                rotation, 
                size,
            ):
            rotation = -rotation
            sn = tf.sin(rotation * (PI / 180))
            csn = tf.cos(rotation * (PI / 180))
            
            rot_matrix = tf.TensorArray(
                tf.float32, 
                size=3, 
                dynamic_size=False,
            )
            rot_matrix = rot_matrix.write(0, value=[csn, -sn, 0])
            rot_matrix = rot_matrix.write(1, value=[sn, csn, 0])
            rot_matrix = rot_matrix.write(2, value=[0, 0, 1])
            rot_matrix = rot_matrix.stack()
            
            tr_matrix = tf.TensorArray(
                tf.float32, 
                size=3, 
                dynamic_size=False,
            )
            tr_matrix = tr_matrix.write(0, value=[1, 0, -size / 2])
            tr_matrix = tr_matrix.write(1, value=[0, 1, -size / 2])
            tr_matrix = tr_matrix.write(2, value=[0, 0, 1])
            tr_matrix = tr_matrix.stack()
            
            inv_matrix = tf.TensorArray(
                tf.float32, 
                size=3, 
                dynamic_size=False,
            )
            inv_matrix = inv_matrix.write(0, value=[1, 0, size / 2])
            inv_matrix = inv_matrix.write(1, value=[0, 1, size / 2])
            inv_matrix = inv_matrix.write(2, value=[0, 0, 1])
            inv_matrix = inv_matrix.stack()

            transfromation_matrix = tf.tensordot(
                tr_matrix, 
                transfromation_matrix, 
                axes=1,
            )
            transfromation_matrix = tf.tensordot(
                rot_matrix, 
                transfromation_matrix, 
                axes=1,
            )
            transfromation_matrix = tf.tensordot(
                inv_matrix, 
                transfromation_matrix, 
                axes=1,
            )
            return transfromation_matrix
        def _expansion_function(image, heatmap, weights):
            weights = tf.expand_dims(weights, axis=0)
            weights = tf.expand_dims(weights, axis=0)
            weights = tf.tile(
                weights, 
                multiples=[heatmap_size, heatmap_size, 1],
            )
            return image, heatmap, weights
        def func(image, joints, weights, loc):
                #joints, weights, loc = label
                center = loc[0:2]
                scale = loc[2]
                #proc = DataPreprocessor(image_size, heatmap_size)
                im, hm, wt = _generating_function(image, joints, weights, center, scale, 0)
                #im = Rescaling(scale=1./255)(im) - mean
                im, hm, wt = _expansion_function(im, hm, wt)
                return im, hm, wt
        return func
            