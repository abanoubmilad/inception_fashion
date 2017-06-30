from glob import glob
from PIL import Image

shift=10

with open("list_landmarks_inshop.txt") as f:
    #f.readline()
    lines = f.readlines()
    counter = 2
    for line in lines:
        temp = line.split()
        name =temp[0]
        parts =name.split('/')
        if parts[1]== 'MEN':
            continue
        im = Image.open(name)
        background = Image.new('RGBA', im.size, (0, 0, 0, 0))
        for i in range(4, len(temp),3):
            x = int(temp[i])
            y = int(temp[i+1])
            background.paste(im.crop((x-shift,y-shift,x+shift,y+shift)),(x-shift,y-shift))
        background.save("img_land_all/"+name.split("/",1)[1])
        print counter
        counter+=1
        break
        #print list2
        #print list1
        #print min(list2),max(list2)
        #print min(list1),max(list1)