from itertools import izip

file1name = 'index_inshop_women_all_bbox_v3.dex'
file2name = 'index_inshop_women_all_land_v3.dex'
file3name = 'index_inshop_women_all_land_bbox_v3.dex'
f = open(file3name, 'w')
with open(file1name) as file1, open(file2name) as file2:
    for line1, line2 in izip(file1, file2): 
        f.write(line1.strip('\n'))
        f.write(" ")
        f.write(line2.split(' ',1)[1])
f.close() 







