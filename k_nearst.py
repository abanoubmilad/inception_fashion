'''


    dev   : Abanoub Milad Nassief
    email : abanoubcs@gmail.com


'''

import numpy as np
import inception_features
import bisect

def get_k_nearst(model_file,img_file,index_file,top_k):
    features= inception_features.get_features(model_file, img_file)
    k_nearst= []
    with open(index_file) as f:
        for line in f:
            feature = line.strip().split(' ')
            arr = np.array(map(float, feature[1:]))
            bisect.insort(k_nearst, (np.linalg.norm(features-arr),feature[0]))
            if len(k_nearst) > top_k:
                k_nearst.pop()
    return [x[1] for x in k_nearst]







