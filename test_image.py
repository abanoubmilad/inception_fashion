from gallery import *
import numpy as np
import fashion_features

images = []
images.append('/media/bono/Scratch/img/WOMEN/Shorts/id_00000022/02_1_front.jpg')
features= fashion_features.get_fashion_features(images)[0]

with open('/home/bono/fashion_cbir.index') as f:
    content = f.readlines()
content = [x.strip() for x in content] 

k_nearst=[]
for line in content:
	feature = line.split(';')
	arr = np.array(map(float, feature[1].strip().split(' ')))
	k_nearst.append((feature[0],np.linalg.norm(features-arr)))

k_nearst = sorted(k_nearst, key=lambda x: x[1], reverse=True)
#print k_nearst
k_nearst = [x[0] for x in k_nearst]
#print k_nearst
show_images(k_nearst[:20])







