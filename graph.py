import numpy as np
import matplotlib.pyplot as plt

import numpy
def smooth(x,window_len=11,window='hanning'):
        if x.ndim != 1:
                raise ValueError, "smooth only accepts 1 dimension arrays."
        if x.size < window_len:
                raise ValueError, "Input vector needs to be bigger than window size."
        if window_len<3:
                return x
        if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
                raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"
        s=numpy.r_[2*x[0]-x[window_len-1::-1],x,2*x[-1]-x[-1:-window_len:-1]]
        if window == 'flat': #moving average
                w=numpy.ones(window_len,'d')
        else:  
                w=eval('numpy.'+window+'(window_len)')
        y=numpy.convolve(w/w.sum(),s,mode='same')
        return y[window_len:-window_len+1]
def get_y_vector(filename):
	top_k=[]
	with open(filename) as f:
		content = f.readlines()
		for line in content:
			top_k.append(line.strip().split(','))
	avr=[]
	tries = len(top_k)
	for i in range(1,51):
		avr.append(sum([int(x[i-1]) for x in top_k])/float(i*tries))
	#print avr
	return avr

x_axis=[i for i in range(1,51)]

plt.plot(x_axis,smooth(np.array(y1)),label="landmarks and bounding box")
plt.plot(x_axis,smooth(np.array(y2)),label="bounding box")
plt.plot(x_axis,smooth(np.array(y3)),label="landmarks")
plt.plot(x_axis,smooth(np.array(y4)),label="full image")

plt.suptitle('CBIR Accuracy vs. top-k retrieved images of DeepFashion\nusing inception v3 architecture')
plt.xlabel('top-k retrieved images')
plt.ylabel('accuracy')

plt.yticks([x / 100.0 for x in range(0, 110, 5)])                                                       
plt.xticks([1]+[x for x in range(5, 60, 5)])                                                       

plt.xlim(xmin=1,xmax=50)
plt.ylim(ymin=0.1,ymax=0.7)

plt.grid()
plt.legend(loc='best')

plt.savefig('results_v3.jpg')
plt.show()