'''


    dev   : Abanoub Milad Nassief
    email : abanoubcs@gmail.com


'''

import numpy as np
import tensorflow as tf

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

def get_features(model_file, img_file):

    with tf.gfile.FastGFile(model_file, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        representation_tensor = sess.graph.get_tensor_by_name('InceptionV4/Logits/AvgPool_1a/AvgPool:0')

        if not tf.gfile.Exists(img_file):
            tf.logging.fatal(' image does not exist %s', img_file)
            return None
        image_data = tf.gfile.FastGFile(img_file, 'rb').read()
        processed_image = preprocess(tf.image.decode_jpeg(image_data, channels=3), 299, 299)
        processed_image = tf.expand_dims(processed_image, 0).eval()
        return np.array(representation_tensor,{'InputImage:0': processed_image})).flatten()







