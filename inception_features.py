'''


    dev   : Abanoub Milad Nassief
    email : abanoubcs@gmail.com


'''

import numpy as np
import tensorflow as tf

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








