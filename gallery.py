from Tkinter import *
from PIL import Image, ImageTk


import subprocess

labels_array=[]
last_canvas_width=-1
IMAGE_DIM=250

def get_screen_resolution():
    output = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',shell=True, stdout=subprocess.PIPE).communicate()[0]
    screen_reso = output.split()[0].split(b'x')
    return [int(screen_reso[0]), int(screen_reso[1])]

def reorder_images(canvas_width):
    global last_canvas_width
    if last_canvas_width != canvas_width and abs(canvas_width-last_canvas_width) >= IMAGE_DIM:
        last_canvas_width = canvas_width
        imgs_per_row=canvas_width/IMAGE_DIM
        img_itr=0
        for label in labels_array:
            label.grid(row=img_itr/imgs_per_row, column=img_itr%imgs_per_row)
            img_itr+=1

def show_images(images_array):
    global labels_array

    reso=get_screen_resolution()

    root =Tk()
    root.wm_title("Inception Fashion")
    #root.minsize(width=reso[0]/4*3, height=reso[1]/3*2)
    #root.geometry('{'+reso[0]/2+'}x{'+reso[1]/2+'}'.format(<widthpixels>, <heightpixels>))
  
    w=reso[0]/4*3
    h=reso[1]/3*2

    root.geometry('%dx%d+%d+%d' % (w, h, (reso[0]-w)/2, (reso[1]-h)/2))
    canvas = Canvas(root, borderwidth=0)
    frame =Frame(canvas)
    vsb =Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0,0), window=frame, anchor="nw")

    
    canvas.update()

    for image in images_array:
        image = Image.open(image)
        image.thumbnail((IMAGE_DIM, IMAGE_DIM), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)

        label = Label(frame, image=photo)
        label.image = photo
        labels_array.append(label)

    reorder_images(int(canvas.winfo_width()))

    frame.bind("<Configure>", lambda event, : canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>", lambda event, :reorder_images(int(canvas.winfo_width())))
    

    #canvas.update()
    #add_images(canvas,frame)

    # for row in range(100):
    #     Label(frame, text="%s" % row, width=3, borderwidth="1", 
    #                  relief="solid").grid(row=row, column=0)
    #     t="this is the second column for row %s" %row
    #     Label(frame, text=t).grid(row=row, column=1)

    root.mainloop()

