import tensorflow as tf
from tensorflow import keras
from keras import layers
from tensorflow.keras import layers

from cv_pose.Models.CVModel import CVModel
#may take parameters, here it takes none
class SoftSkipConv(CVModel):
    def getModel(momentum=0.9, epsilon = 0.001, kernel_initializer = 'glorot_uniform', num_filters = 144, 
        dropout_rate = 0.2, num_stacks = 4, img_size = 256):
        def skip_block(inputs, filters):
            x1 = layers.BatchNormalization(
                momentum=momentum, 
                epsilon=epsilon, 
                scale=False,
                )(inputs)
            x1 = layers.ReLU()(x1)
            x1 = layers.Conv2D(
                filters=int(filters/2), 
                kernel_size=(3,3), 
                strides=(1,1), 
                padding='same',
                kernel_initializer=kernel_initializer,
                )(x1)
            
            x2 = layers.BatchNormalization(
                momentum=momentum, 
                epsilon=epsilon, 
                scale=False,
                )(x1)
            x2 = layers.ReLU()(x2)
            x2 = layers.Conv2D(
                filters=int(filters/4), 
                kernel_size=(3,3), 
                strides=(1,1), 
                padding='same',
                kernel_initializer=kernel_initializer,
                )(x2)

            x3 = layers.BatchNormalization(
                momentum=momentum, 
                epsilon=epsilon, 
                scale=False,
                )(x2)
            x3 = layers.ReLU()(x3)
            x3 = layers.Conv2D(
                filters=int(filters/4),
                kernel_size=(3,3), 
                strides=(1,1), 
                padding='same',
                kernel_initializer=kernel_initializer,
                )(x3)
            x = layers.concatenate(
                [x1, x2, x3], 
                axis=3,
            )

            if inputs.shape[3] == x.shape[3]:
                skip = layers.DepthwiseConv2D(
                    kernel_size=1, 
                    strides=(1,1), 
                    depthwise_initializer=kernel_initializer,
                    )(inputs)
            else:
                skip = layers.Conv2D(
                    filters=int(filters), 
                    kernel_size=(1,1), 
                    strides=(1,1), 
                    kernel_initializer=kernel_initializer,
                    )(inputs)
            return tf.math.add_n([x, skip])
        
        def encoder(inputs):
            skip1 = skip_block(inputs, filters=inputs.shape[3])
            e1 = layers.MaxPool2D(pool_size=(2,2))(inputs)
            e1 = skip_block(e1, filters=e1.shape[3])
            
            skip2 = skip_block(e1, filters=e1.shape[3])
            e2 = layers.MaxPool2D(pool_size=(2,2))(e1)
            e2 = skip_block(e2, filters=e2.shape[3]//2) 

            skip3 = skip_block(e2, filters=e2.shape[3])
            e3 = layers.MaxPool2D(pool_size=(2,2))(e2)
            e3 = skip_block(e3, filters=e3.shape[3]) 

            skip4 = skip_block(e3, filters=e3.shape[3])
            e4 = layers.MaxPool2D(pool_size=(2,2))(e3)
            e4 = skip_block(e4, filters=e4.shape[3]) 

            return e4, skip1, skip2, skip3, skip4
        
        def decoder(e_out, skip1, skip2, skip3, skip4):
            d4 = layers.UpSampling2D(size=(2,2))(e_out)
            d4 = layers.concatenate(
                [skip4, d4], 
                axis=3,
            )
            d4 = layers.Conv2D(
                filters=int(d4.shape[3]/2), 
                kernel_size=(3,3), 
                strides=(1,1), 
                padding='same',
                kernel_initializer=kernel_initializer,
                )(d4)
            d4 = skip_block(d4, filters=d4.shape[3])            

            d3 = layers.UpSampling2D(size=(2,2))(d4)
            d3 = layers.concatenate(
                [skip3, d3], 
                axis=3,
            )
            d3 = layers.Conv2D(
                filters=int(d3.shape[3]/2), 
                kernel_size=(3,3), 
                strides=(1,1), 
                padding='same',
                kernel_initializer=kernel_initializer,
                )(d3)
            d3 = skip_block(d3, filters=d3.shape[3]*2)            

            d2 = layers.UpSampling2D(size=(2,2))(d3)
            d2 = layers.concatenate(
                [skip2, d2], 
                axis=3,
            )
            d2 = layers.Conv2D(
                filters=int(d2.shape[3]/2), 
                kernel_size=(3,3), 
                strides=(1,1), 
                padding='same',
                kernel_initializer=kernel_initializer,
                )(d2)
            d2 = skip_block(d2, filters=d2.shape[3])           

            d1 = layers.UpSampling2D(size=(2,2))(d2)
            d1 = layers.concatenate(
                [skip1, d1], 
                axis=3,
            )
            d1 = layers.Conv2D(
                filters=int(d1.shape[3]/2), 
                kernel_size=(3,3), 
                strides=(1,1), 
                padding='same',
                kernel_initializer=kernel_initializer,
                )(d1)
            return skip_block(d1, filters=d1.shape[3])     
        
        def bottleneck(inputs, final=tf.constant(0)):
            e_out, skip1, skip2, skip3, skip4 = encoder(inputs)
            x = decoder(e_out, skip1, skip2, skip3, skip4)
            x = layers.Dropout(rate=dropout_rate)(x)
            x = skip_block(x, tf.cast(num_filters, tf.int32))
            x = layers.Conv2D(
                filters=num_filters,
                kernel_size=(1,1),
                strides=(1,1),
                kernel_initializer=kernel_initializer,
                )(x)
            x = layers.BatchNormalization(
                momentum=momentum, 
                epsilon=epsilon, 
                scale=False,
                )(x)
            x = layers.ReLU()(x)
            scores = layers.Conv2D(
                filters=num_joints,
                kernel_size=(1,1),
                strides=(1,1),
                kernel_initializer=kernel_initializer,
                )(x)
            if final == 0:
                x_lower = layers.Conv2D(
                    filters=num_filters,
                    kernel_size=(1,1),
                    strides=(1,1),
                    kernel_initializer=kernel_initializer,
                    )(scores)
                x_upper = layers.Conv2D(
                    filters=num_filters,
                    kernel_size=(1,1),
                    strides=(1,1),
                    kernel_initializer=kernel_initializer,
                    )(x)
                x = layers.Add()([
                    x_lower, 
                    x_upper, 
                    inputs,
                ])
                return scores, x
            else:
                return scores

        num_joints = 16
        inputs = tf.keras.layers.Input([
           img_size, 
           img_size, 
            3,
        ])
        outputs = None
        x = layers.ZeroPadding2D(padding=(3,3))(inputs)
        x = layers.Conv2D(
            filters=num_filters//4,
            kernel_size=(7,7),
            strides=(2,2),
            kernel_initializer=kernel_initializer,
            )(x)
        x = layers.BatchNormalization(
            momentum=momentum, 
            epsilon=epsilon,                                               
            scale=False,
            )(x)
        x = layers.ReLU()(x)

        x = skip_block(x, tf.cast(num_filters / 2, tf.int32))
        x = layers.MaxPool2D(
            pool_size=(2,2), 
            strides=(2,2),
            )(x)
        x = skip_block(x, tf.cast(num_filters, tf.int32))
        x = skip_block(x, tf.cast(num_filters,tf.int32))

        hm1, x = bottleneck(x)
        if num_stacks == 8:
            hm2, x = bottleneck(x, final=tf.constant(0))
            hm3, x = bottleneck(x, final=tf.constant(0))
            hm4, x = bottleneck(x, final=tf.constant(0))
            hm5, x = bottleneck(x, final=tf.constant(0))
            hm6, x = bottleneck(x, final=tf.constant(0))
            hm7, x = bottleneck(x, final=tf.constant(0))
            hm8 = bottleneck(x, final=tf.constant(1))
            outputs = tf.stack(
                [hm1, hm2, hm3, hm4, hm5, hm6, hm7, hm8], 
                axis=1,
            )
        elif num_stacks == 4:
            hm2, x = bottleneck(x)
            hm3, x = bottleneck(x)
            hm4 = bottleneck(x, final=tf.constant(1))
            outputs =  tf.stack(
                [hm1, hm2, hm3, hm4], 
                axis=1,
            )
        else:
            hm2 = bottleneck(x, final=tf.constant(1))
            outputs = tf.stack(
                [hm1, hm2], 
                axis=1,
            )
        outputs = layers.Activation(
        'linear', 
        dtype='float32',
        )(outputs)
        return tf.keras.Model(inputs, outputs)

