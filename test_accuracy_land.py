'''

    test_image.py
    calls gallery with KTH_NEARST fashion images

    dev   : Abanoub Milad Nassief
    email : abanoubcs@gmail.com


'''
from glob import glob
import gallery
import k_nearst
import numpy as np
import inception_features
import bisect
import sys
import os

if __name__ == "__main__":

	#if len(sys.argv) != 5 :
	#	print 'err, test_accuracy.py <model_file> <index_file> <input_folder_with_cats> <output_file>'
	#	exit()

	model_file = "incep_v3.pb"
	index_file = "index_inshop_women_all_land_bbox_v3.dex"
	input_folder = "/media/bono/Scratch/gp/In-shop_Clothes_Retrieval_Benchmark/Img/img_BBOX/WOMEN"
	output_file = "inshop_all_land_bbox_v3_results.csv"
	fout=open(output_file,'w')
	top_k=51
	per_class=10
	images =[]
	images_land=[]
	coun2=0
	for cat in glob(input_folder+'/*'):
		coun=0
		for path, subdirs, files in os.walk(cat):
			for name in files:
				if coun < per_class:
					coun+=1
					coun2+=1
					tmp=os.path.join(path, name)
					images.append(tmp.replace("img_BBOX","img_bbox_all"))
					images_land.append(tmp.replace("img_BBOX","img_all_land"))
				else:
					break
	print coun2,"#############"
	features_arr= inception_features.get_features_arr_land(model_file, images,images_land)
	print 'fetched all features'
	total =0
	success=0
	for features, image_path in zip(features_arr, images):
		with open(index_file) as f:
			k_nearst= []
			for line in f:
				feature = line.strip().split(' ')
				arr = np.array(map(float, feature[1:]))
				bisect.insort(k_nearst, (np.linalg.norm(features-arr),feature[0]))
				if len(k_nearst) > top_k:
					k_nearst.pop()
			last_cat=image_path.split('/')
			last_cat=last_cat[len(last_cat)-3]
			# print last_cat,'\n'
			# print k_nearst,'\n'
			temp =0
			counter=0
			for x in k_nearst[1:]:
				counter+=1
				# print x[1],'\n'
				if last_cat in x[1]:
					temp+=1
				if counter == 1:
					fout.write(str(temp))
				elif counter == top_k-1:
					fout.write(','+str(temp)+'\n')
				else:
					fout.write(','+str(temp))	
			# if temp >1:
			# 	success+=1
			# # print 'success ',success
			# print success/float(total) *100,"%"
			total+=1
			print 'image',total


# k = k_nearst.get_k_nearst('incep_v3.pb',
# image_paths[0],'index_101cat_v3.dx',2)

# last_cat=image_paths[0].split('/')
# last_cat=last_cat[len(last_cat)-2]
# print last_cat,'\n'
# for i in k:
# 	print i,'\n'
# 	if last_cat in i:
# 		temp+=1

# print 'temp',temp, 
# total+=1







