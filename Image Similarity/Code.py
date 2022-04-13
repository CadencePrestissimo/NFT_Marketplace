from tkinter import *
from PIL import Image, ImageTk, ImageDraw
import tkinter.filedialog as tkFileDialog
import cv2
import sewar
import requests

# make a tkinter gui with options to upload two image from local system
# and compare them
# there will be two load button for both images , they will be shown side by side to each other in the GUI
# and the result will be shown in the bottom of the GUI
Image1=None
Image2=None



class Paint(object):
    MARKER_COLOR = 'white'

    def __init__(self):

        self.root = Tk()

        self.poly_button = Button(self.root, text='Load Image 1', command=lambda:self.load(1), width=12, height=3)
        self.poly_button.grid(row=1, column=2)
        self.imageDict={}
        self.revoke_button = Button(self.root, text='Load Image 2', command=lambda:self.load(2), width=12, height=3)
        self.revoke_button.grid(row=2, column=2)

        self.clear_button = Button(self.root, text='Clear', command=self.clear, width=12, height=3)
        self.clear_button.grid(row=3, column=2)

        self.c = Canvas(self.root, bg='white', width=408, height=400)
        self.c.grid(row=0, column=0, rowspan=8)

        self.out = Canvas(self.root, bg='white', width=408, height=400)
        self.out.grid(row=0, column=1, rowspan=8)

        self.save_button = Button(self.root, text="Get Similarity", command=lambda:self.getSimilarity(), width=12, height=3)
        self.save_button.grid(row=6, column=2)

        
        self.filename = None

        # self.setup()
        self.root.mainloop()

    def clear(self):
        self.c.delete("all")
        self.out.delete("all")

    def load(self,num):
        self.filename = tkFileDialog.askopenfilename(initialdir='./imgs',
                                                     title="Select file",
                                                     filetypes=(("png files", "*.png"), ("jpg files", "*.jpg"),
                                                                ("all files", "*.*")))
        self.filename_ = self.filename.split('/')[-1][:-4]
        self.filepath = '/'.join(self.filename.split('/')[:-1])
        print(self.filename_, self.filepath,num)
        cv2.imwrite('image'+str(num)+'.jpg',cv2.imread(self.filename))
        try:
            photo = Image.open(self.filename)
            w, h = photo.size
        
            self.imageDict['image'+str(num)] = cv2.imread(self.filename)
            photo=photo.resize((400,400), Image.ANTIALIAS)
        except:
            print('Do not load image')
        if num==1:
            # print(photo.)
            self.image1 = ImageTk.PhotoImage(photo)
            # self.imag
            self.c.create_image(0, 0, image=self.image1, anchor=NW)
        else:
            self.image2 = ImageTk.PhotoImage(photo)
            self.out.create_image(0, 0, image=self.image2, anchor=NW)
        
    def getSimilarity(self):
        if self.image1==None or self.image2==None:
            print('Both Images needs to be chosen.')
            return
        r = requests.post(
        "https://api.deepai.org/api/image-similarity",
        files={
            'image1': open('./image1.jpg', 'rb'),
            'image2': open('./image2.jpg', 'rb'),
        },
        headers={'api-key': 'd7d7f4b0-ea40-48b6-b84c-5543d41c661a'}
        )
        # print(r.json())
        per=int(r.json().get('output').get('distance'))
        print(100-per)



if __name__ == '__main__':
    ge = Paint()