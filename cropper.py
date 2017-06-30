from glob import glob
from PIL import Image

with open("/media/bono/Scratch/gp/In-shop_Clothes_Retrieval_Benchmark/Img/list_bbox_inshop.txt") as f:
    f.readline()
    f.readline()
    f.readline()
    lines = f.readlines()
    counter = 1
    for line in lines:
        temp = line.split()
        name =temp[0]
        parts =name.split('/')
        if parts[1]== 'MEN':
            continue
        im = Image.open(name)
        tempImage = im.crop((int(temp[3]),int(temp[4]),int(temp[5]),int(temp[6])))
        tempImage.save(name)
        counter+=1
        print counter