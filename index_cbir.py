'''

    index_cbir.py
    extracts features of images located in cats_path
    and creates and index file located index_path
    that holds each images and its associated features vector
    
    dev   : Abanoub Milad Nassief
    email : abanoubcs@gmail.com


'''

from glob import glob
import fashion_features
import json
import numpy as np
import tensorflow as tf

PICS_PER_CAT=10000
cats_path='/home/bono/fashion/women/'
index_path='/home/bono/fashion_cbir.index'
cats=glob(cats_path+'/*')

images_array = []
for cat in cats:
    itr=0         
    for pic in glob(cat+'/*'):
        if itr == PICS_PER_CAT:
            break   
        itr+=1
        images_array.append(pic)
        
print len(images_array), ' images found'

index_file=open(index_path,'w')




modelFullPath = '/tmp/output_graph.pb'
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
        image_data = tf.gfile.FastGFile(image_path, 'rb').read()
        
        index_file.write(image_path+';')
        for item in np.array(sess.run(representation_tensor,{'DecodeJpeg/contents:0': image_data})).flatten():
            index_file.write(" %s" % item)
        index_file.write('\n')
        print 'image num. ',total, ' done'
        # if total ==3:
        #     break
        total+=1
    #np.set_printoptions(threshold=np.inf)

index_file.close() 






