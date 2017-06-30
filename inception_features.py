'''


    dev   : Abanoub Milad Nassief
    email : abanoubcs@gmail.com


'''

import numpy as np
import tensorflow as tf
from itertools import izip

def get_features(model_file, img_file):

    with tf.gfile.FastGFile(model_file, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        representation_tensor = sess.graph.get_tensor_by_name('pool_3/_reshape:0')

        if not tf.gfile.Exists(img_file):
            tf.logging.fatal(' image does not exist %s', img_file)
            return None
        image_data = tf.gfile.FastGFile(img_file, 'rb').read()
        return np.array(sess.run(representation_tensor,{'DecodeJpeg/contents:0': image_data})).flatten()

def get_features_land(model_file, img_file,img_file_land):

    with tf.gfile.FastGFile(model_file, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        representation_tensor = sess.graph.get_tensor_by_name('pool_3/_reshape:0')

        if not tf.gfile.Exists(img_file):
            tf.logging.fatal(' image does not exist %s', img_file)
            return None
        if not tf.gfile.Exists(img_file_land):
            tf.logging.fatal(' image does not exist %s', img_file_land)
            return None
        arr1= np.array(sess.run(representation_tensor,{'DecodeJpeg/contents:0': tf.gfile.FastGFile(img_file, 'rb').read()})).flatten()
        arr2= np.array(sess.run(representation_tensor,{'DecodeJpeg/contents:0': tf.gfile.FastGFile(img_file_land, 'rb').read()})).flatten()
        return np.concatenate([arr1,arr2])
        
def get_features_arr(model_file, img_file_arr):
    itr=0
    with tf.gfile.FastGFile(model_file, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    output_arr=[]
    with tf.Session() as sess:
        representation_tensor = sess.graph.get_tensor_by_name('pool_3/_reshape:0')
        for img_file in img_file_arr:
            itr+=1
            if not tf.gfile.Exists(img_file):
                tf.logging.fatal(' image does not exist %s', img_file)
                return None
            image_data = tf.gfile.FastGFile(img_file, 'rb').read()
            output_arr.append(np.array(sess.run(representation_tensor,{'DecodeJpeg/contents:0': image_data})).flatten())
            # if itr >100:
            #     break
    return output_arr

def get_features_arr_land(model_file, img_file_arr,img_file_arr_land):
    itr=0
    with tf.gfile.FastGFile(model_file, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    output_arr=[]
    with tf.Session() as sess:
        representation_tensor = sess.graph.get_tensor_by_name('pool_3/_reshape:0')
        for img_file,img_file_land in izip(img_file_arr, img_file_arr_land): 
            if not tf.gfile.Exists(img_file):
                tf.logging.fatal(' image does not exist %s', img_file)
                return None
            if not tf.gfile.Exists(img_file_land):
                tf.logging.fatal(' image does not exist %s', img_file_land)
                return None
            arr1= np.array(sess.run(representation_tensor,{'DecodeJpeg/contents:0': tf.gfile.FastGFile(img_file, 'rb').read()})).flatten()
            arr2= np.array(sess.run(representation_tensor,{'DecodeJpeg/contents:0': tf.gfile.FastGFile(img_file_land, 'rb').read()})).flatten()
            output_arr.append(np.concatenate([arr1,arr2]))
    return output_arr





