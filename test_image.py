'''

    test_image.py
    extracts features of IMG_PATH then calls gallery with KTH_NEARST fashion images

    dev   : Abanoub Milad Nassief
    email : abanoubcs@gmail.com


'''

from gallery import *
import numpy as np
import fashion_features
import bisect

KTH_NEARST=50
IMG_PATH = '/home/bono/Desktop/hol_91072_01_model1.jpg'

features= fashion_features.get_fashion_features([IMG_PATH])[0]

with open('/home/bono/fashion_cbir.index') as f:
    content = f.readlines()
content = [x.strip() for x in content] 

k_nearst= []

for line in content:
	feature = line.split(';')
	arr = np.array(map(float, feature[1].strip().split(' ')))
	bisect.insort(k_nearst, (np.linalg.norm(features-arr),feature[0]))
	if len(k_nearst) > KTH_NEARST:
		k_nearst.pop()

show_images([x[1] for x in k_nearst],IMG_PATH)







