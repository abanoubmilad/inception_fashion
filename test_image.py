'''

    test_image.py
    calls gallery with KTH_NEARST fashion images

    dev   : Abanoub Milad Nassief
    email : abanoubcs@gmail.com


'''

import gallery
import k_nearst

img_path_test="Dresses/id_00000866/01_1_front.jpg"
IMG_PATH_bbox = 'img_bbox_all/WOMEN/'+img_path_test
org_IMG_PATH = 'img/WOMEN/'+img_path_test
#IMG_PATH_LAND = 'img_land/WOMEN/'+img_path_test

image_paths = k_nearst.get_k_nearst('incep_v3.pb',
    IMG_PATH_bbox,
   	'index_inshop_women_all_bbox_v3.dex',
   	50)

gallery.show_images(image_paths,org_IMG_PATH)







