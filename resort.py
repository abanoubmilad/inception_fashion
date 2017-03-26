from glob import glob
import os, sys
from shutil import copyfile

def resort(src, des):
    os.makedirs(des)
    itr=0

    for cat in glob(src+'/*'):
        dest=des+'/'+cat.rsplit('/',1)[1]+'/'
        os.makedirs(dest)
        for sub_cat in glob(cat+'/*'):
            for pic in glob(sub_cat+'/*'):
                copyfile(pic, dest+str(itr))
                itr+=1


if __name__ == "__main__":
   resort(sys.argv[1],sys.argv[2])