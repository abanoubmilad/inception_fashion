'''

    
    dev   : Abanoub Milad Nassief
    email : abanoubcs@gmail.com


'''

from glob import glob
import numpy as np
import tensorflow as tf
import sys
def preprocess(image, height, width,
                        central_fraction=0.875, scope=None):
  """Prepare one image for evaluation.

  If height and width are specified it would output an image with that size by
  applying resize_bilinear.

  If central_fraction is specified it would cropt the central fraction of the
  input image.

  Args:
    image: 3-D Tensor of image. If dtype is tf.float32 then the range should be
      [0, 1], otherwise it would converted to tf.float32 assuming that the range
      is [0, MAX], where MAX is largest positive representable number for
      int(8/16/32) data type (see `tf.image.convert_image_dtype` for details)
    height: integer
    width: integer
    central_fraction: Optional Float, fraction of the image to crop.
    scope: Optional scope for name_scope.
  Returns:
    3-D float Tensor of prepared image.
  """
  with tf.name_scope(scope, 'eval_image', [image, height, width]):
    if image.dtype != tf.float32:
      image = tf.image.convert_image_dtype(image, dtype=tf.float32)
    # Crop the central region of the image with an area containing 87.5% of
    # the original image.
    if central_fraction:
      image = tf.image.central_crop(image, central_fraction=central_fraction)

    if height and width:
      # Resize the image to the specified height and width.
      image = tf.expand_dims(image, 0)
      image = tf.image.resize_bilinear(image, [height, width],
                                       align_corners=False)
      image = tf.squeeze(image, [0])
    image = tf.subtract(image, 0.5)
    image = tf.multiply(image, 2.0)
    return image


def index_path_url(model_file, input_path_url_file, output_index_file, is_v3=True):

    with tf.gfile.FastGFile(model_file, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    fout = open(output_index_file,'w') 
    with tf.Session() as sess:
        if is_v3:
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
        else:
            representation_tensor = sess.graph.get_tensor_by_name('InceptionV4/Logits/AvgPool_1a/AvgPool:0')

            total = 1
            with open(input_file) as fin:
                for line in fin:
                    tmp= line.strip().split(' ')
                    if not tf.gfile.Exists(tmp[0]):
                        tf.logging.fatal(' image does not exist %s', tmp[0])
                    image_data = tf.gfile.FastGFile(tmp[0], 'rb').read()
                    processed_image = preprocess(tf.image.decode_jpeg(image_data, channels=3), 299, 299)
                    processed_image = tf.expand_dims(processed_image, 0).eval()

                    fout.write(tmp[1])
                    for item in np.array(sess.run(representation_tensor,
                        {'InputImage:0': processed_image})).flatten():
                        fout.write(" %s" % item)
                    fout.write('\n')
                    print 'image num. ',total, ' done'
                    # if total ==3:
                    #     break
                    total+=1
                    #np.set_printoptions(threshold=np.inf)

    fout.close() 

def index_folder(model_file, input_folder, output_index_file, is_v3=True):

    with tf.gfile.FastGFile(model_file, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    fout=open(output_index_file,'w')
    total =1
    with tf.Session() as sess:
        if is_v3:
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
        else:
            representation_tensor = sess.graph.get_tensor_by_name('InceptionV4/Logits/AvgPool_1a/AvgPool:0')
            for cat in glob(input_folder+'/*'):
                for sub_cat in glob(cat+'/*'):
                    for image_path in glob(sub_cat+'/*'):
                        if not tf.gfile.Exists(image_path):
                            tf.logging.fatal(' image does not exist %s', image_path)
                        image_data = tf.gfile.FastGFile(image_path, 'rb').read()
                        processed_image = preprocess(tf.image.decode_jpeg(image_data, channels=3), 299, 299)
                        processed_image = tf.expand_dims(processed_image, 0).eval()
                        fout.write(image_path)
                        for item in np.array(sess.run(representation_tensor,
                        {'InputImage:0': processed_image})).flatten():
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




