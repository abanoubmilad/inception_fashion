'''

    test_image.py
    calls gallery with KTH_NEARST fashion images

    dev   : Abanoub Milad Nassief
    email : abanoubcs@gmail.com


'''

import gallery
import k_nearst

IMG_PATH = '/home/bono/Desktop/f8c9e779b0f70260af54535a4b37f1fd.jpg'

image_paths = k_nearst.get_k_nearst('output_graph.pb',
    IMG_PATH,
   	'fashion_cbir.index',
   	20)

gallery.show_images(image_paths,IMG_PATH)







