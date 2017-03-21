'''

    predict_image.py
    predicts class of given image
    
    dev   : Abanoub Milad Nassief
    email : abanoubcs@gmail.com


'''

import numpy as np
import tensorflow as tf
import sys
import time

imagePath = ''
modelFullPath = '/tmp/output_graph.pb'
labelsFullPath = '/tmp/output_labels.txt'


def create_graph():
    with tf.gfile.FastGFile(modelFullPath, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def run_inference_on_image():
    answer = None

    if not tf.gfile.Exists(imagePath):
        tf.logging.fatal(' File does not exist %s', imagePath)
        return answer

    image_data = tf.gfile.FastGFile(imagePath, 'rb').read()

    create_graph()

    with tf.Session() as sess:
        representation_tensor = sess.graph.get_tensor_by_name('pool_3/_reshape:0')
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        [features, predictions] = sess.run([representation_tensor, softmax_tensor],
         {'DecodeJpeg/contents:0': image_data})

        # representation_tensor = sess.graph.get_tensor_by_name('pool_3/_reshape:0')
        # features = sess.run(representation_tensor,
        #                        {'DecodeJpeg/contents:0': image_data})
        #print(features.shape)
        np.set_printoptions(threshold=np.inf)
        features = np.array(features).flatten()
        print(features)
       # features = np.squeeze(representation_tensor)

        #sys.exit()

        # softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        # predictions = sess.run(softmax_tensor,
        #                        {'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)

        top_k = predictions.argsort()[-5:][::-1]  # Getting top 5 predictions
        f = open(labelsFullPath, 'rb')
        lines = f.readlines()
        labels = [str(w).replace("\n", "") for w in lines]
        for node_id in top_k:
            human_string = labels[node_id]
            score = predictions[node_id]
            print('%.2f%% %s' % (score*100, human_string))

        answer = labels[top_k[0]]
        return answer


if __name__ == '__main__':
    
    if len(sys.argv)!=2:
        tf.logging.fatal(' Invalid number of arguments,\nusage: python test_me.py imageFullPath')
        sys.exit()
    imagePath = sys.argv[1]
    print ('\nworking on image ...\n')
    start_time = time.time()
    run_inference_on_image()
    print ' '
    print ('took %f seconds\n'%(time.time() - start_time))

    # cbir l2

    #dist = np.linalg.norm(a-b)
