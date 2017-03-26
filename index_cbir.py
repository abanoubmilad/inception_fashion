'''

    
    dev   : Abanoub Milad Nassief
    email : abanoubcs@gmail.com


'''

from glob import glob
import numpy as np
import tensorflow as tf
import sys

def index_path_url(model_file, input_path_url_file, output_index_file):

    with tf.gfile.FastGFile(model_file, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    fout = open(output_index_file,'w') 
    with tf.Session() as sess:
        representation_tensor = sess.graph.get_tensor_by_name('pool_3/_reshape:0')

        total = 1
        with open(input_file) as fin:
            for line in fin:
                tmp= line.strip().split(' ')
                if not tf.gfile.Exists(tmp[0]):
                    tf.logging.fatal(' image does not exist %s', tmp[0])
                image_data = tf.gfile.FastGFile(tmp[0], 'rb').read()
                
                fout.write(tmp[1])
                for item in np.array(sess.run(representation_tensor,{'DecodeJpeg/contents:0': image_data})).flatten():
                    fout.write(" %s" % item)
                fout.write('\n')
                print 'image num. ',total, ' done'
                # if total ==3:
                #     break
                total+=1
                #np.set_printoptions(threshold=np.inf)

    fout.close() 

def index_folder(model_file, input_folder, output_index_file):

    with tf.gfile.FastGFile(model_file, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    fout=open(output_index_file,'w')
    total =1
    with tf.Session() as sess:
        representation_tensor = sess.graph.get_tensor_by_name('pool_3/_reshape:0')
        for cat in glob(input_folder+'/*'):
            for sub_cat in glob(cat+'/*'):
                for image_path in glob(sub_cat+'/*'):
                    if not tf.gfile.Exists(image_path):
                        tf.logging.fatal(' image does not exist %s', image_path)
                    image_data = tf.gfile.FastGFile(image_path, 'rb').read()
                    
                    fout.write(image_path)
                    for item in np.array(sess.run(representation_tensor,{'DecodeJpeg/contents:0': image_data})).flatten():
                        fout.write(" %s" % item)
                    fout.write('\n')
                    print 'image num. ',total, ' done'
                    # if total ==3:
                    #     exit()
                    total+=1
    fout.close() 

if __name__ == "__main__":
    # if len(sys.argv) != 4 :
    #     print 'err, index_path_url.py  <model_file>  <input_file>  <output_file>'
    #     exit()
    # index_path_url(sys.argv[1],sys.argv[2],sys.argv[3])

    if len(sys.argv) != 4 :
        print 'err, index_folder.py  <model_file>  <input_folder>  <output_file>'
        exit()
    index_folder(sys.argv[1],sys.argv[2],sys.argv[3])




