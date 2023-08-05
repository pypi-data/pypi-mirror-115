import os
import numpy as np
from scipy import ndimage, interpolate
from scipy.ndimage import zoom
#import time
#import random
#import math
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Conv3D, MaxPooling3D, Conv3DTranspose, concatenate
import tensorflow.keras.backend as K
from processing import *


def SOUP_GAN(thicks_ori, Z_FAC):

    thicks_ori = rescale_img(thicks_ori, max_val= 10000)

    thins = zoom(thicks_ori, (1,1,Z_FAC))

    new_model=keras.models.load_model('./Thin-to-thin')
    thins_gen = thins.copy()

    target = np.moveaxis(thins,-1,0)
    target = target [...,np.newaxis]
    target = target [np.newaxis,...]

    index  = attention_coeff(target, Z_FAC)

    target = new_model.predict([target,index])
     
    target_small = target[0,...,0]
    thins_gen = np.moveaxis(target_small, 0,-1)

    return thins_gen
     



