import numpy as np
import tensorflow as tf

modelFullPath = '/tmp/output_graph.pb'

def get_fashion_features(images_array):
    features_array = []

    # Creates graph from saved GraphDef.
    with tf.gfile.FastGFile(modelFullPath, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        representation_tensor = sess.graph.get_tensor_by_name('pool_3/_reshape:0')

        total = 1
        for image_path in images_array:
            if not tf.gfile.Exists(image_path):
                tf.logging.fatal(' image does not exist %s', image_path)
                return None
            image_data = tf.gfile.FastGFile(image_path, 'rb').read()
            features_array.append(np.array(sess.run(representation_tensor,{'DecodeJpeg/contents:0': image_data})).flatten())
            print 'image num. ',total, ' done'
            total+=1
        #np.set_printoptions(threshold=np.inf)
        return features_array








