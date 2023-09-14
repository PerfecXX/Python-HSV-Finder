import cv2
from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
import numpy as np
import pyperclip
# Camera Index
camIndex = 0

def get_lowerRange():
    lowerRange = '{},{},{}'.format(get_lh(),get_ls(),get_lv())
    pyperclip.copy(lowerRange)

def get_upperRange():
    upperRange = '({},{},{})'.format(get_uh(),get_us(),get_uv())
    pyperclip.copy(upperRange)
    

def flip_cam():
    global cap
    # Read a frame from the video capture
    ret, frame = cap.read()
    # Flip the frame horizontally
    frame = cv2.flip(frame, 1)

def next_cam():
    global camIndex,cap
    camIndex +=1
    cap.release()
    cap = cv2.VideoCapture(camIndex)
    camChLabel.config(text='CH:{}'.format(camIndex))

def prev_cam():
    global camIndex,cap
    camIndex -=1
    if camIndex <0:
        messagebox.showerror("Error! Camera Chanel Limitation!", "No previous camera")
        camIndex = 0
    else:
        cap.release()
        cap = cv2.VideoCapture(camIndex)
        camChLabel.config(text='CH:{}'.format(camIndex))

def update_frame():
    # Read a frame from the video capture
    ret, frame = cap.read()
    
    # Get the lower and upper bound values from the sliders
    lower_bound = np.array([l_h.get(), l_s.get(), l_v.get()])
    upper_bound = np.array([u_h.get(), u_s.get(), u_v.get()])
    
    # Convert the frame to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Get the binary mask
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    
    # Filter the original frame using the mask
    filtered_frame = cv2.bitwise_and(frame, frame, mask=mask)
    
    # Convert the filtered frame to grayscale
    gray = cv2.cvtColor(filtered_frame, cv2.COLOR_BGR2GRAY)

    # Threshold the grayscale image to get a binary image
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)


    # Convert the frame to a PhotoImage object
    img1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img1 = Image.fromarray(img1)
    img1 = ImageTk.PhotoImage(image=img1)
    
    # Convert the filtered frame to a PhotoImage object
    img2 = cv2.cvtColor(filtered_frame, cv2.COLOR_BGR2RGB)
    img2 = Image.fromarray(img2)
    img2 = ImageTk.PhotoImage(image=img2)
    
    # Convert the binary image to a PhotoImage object
    img3 = cv2.cvtColor(binary, cv2.COLOR_GRAY2RGB)
    img3 = Image.fromarray(img3)
    img3 = ImageTk.PhotoImage(image=img3)

    # Update the label's image
    vidLabel1.config(image=img1)
    vidLabel1.image = img1
    
    # Update the label's image with the filtered frame
    vidLabel2.config(image=img2)
    vidLabel2.image = img2
    
    vidLabel3.config(image=img3)
    vidLabel3.image = img3
    
    # Schedule the next frame update
    window.after(10, update_frame)

    
# Create the main window
window = Tk()
window.geometry('910x600')
window.title('HSV Range Finder')
window.resizable(0,0)

# ---Camera frame---
mainCameraFrame = LabelFrame(text='Main Camera')
mainCameraFrame.place(x=0,y=0)

# Video label to camera frame
vidLabel1 = Label(mainCameraFrame)
vidLabel1.configure(width=300, height=400)
vidLabel1.pack()

# --- Contour frame---
contourCameraFrame = LabelFrame(text='Result Camera')
contourCameraFrame.place(x=305,y=0)

# Video label to camera frame
vidLabel2 = Label(contourCameraFrame)
vidLabel2.configure(width=300, height=400)
vidLabel2.pack()

# --- Output---
outCameraFrame = LabelFrame(text='Binary Mask')
outCameraFrame.place(x=600,y=0)

# Video label to camera frame
vidLabel3 = Label(outCameraFrame)
vidLabel3.configure(width=300, height=400)
vidLabel3.pack()


# ---Camera Control Frame---
cameraControlFrame = LabelFrame(text='Camera Control')
cameraControlFrame.place(x=0,y=425)

# Camera chanel label
camChLabel = Label(cameraControlFrame,text='CH:0',font=('',25,'bold'))
camChLabel.grid(row=0,column=0,columnspan=2)
# Button
nextCambtn = Button(cameraControlFrame,text='Prev Camera',command=prev_cam)
nextCambtn.grid(row=1,column=0)
prevCambtn = Button(cameraControlFrame,text='Next Camera',command=next_cam)
prevCambtn.grid(row=1,column=1)
flipHCambtn = Button(cameraControlFrame,text='Flip Horizontal',command=flip_cam)
flipHCambtn.grid(row=2,column=0)
flipVCambtn = Button(cameraControlFrame,text='Flip Vertical',command=...)
flipVCambtn.grid(row=2,column=1)

# ---Slider---

# Slide Bar Variable
l_h,l_s,l_v = DoubleVar(),DoubleVar(),DoubleVar()
u_h,u_s,u_v = DoubleVar(),DoubleVar(),DoubleVar()

# Set the default values of the upper bound sliders
u_h.set(179)
u_s.set(255)
u_v.set(255)

def get_lh():
    return '{:.0f}'.format(l_h.get())

def lh_changed(event):
    lhShow.configure(text=get_lh())

def get_ls():
    return '{:.0f}'.format(l_s.get())

def ls_changed(event):
    lsShow.configure(text=get_ls())

def get_lv():
    return '{:.0f}'.format(l_v.get())

def lv_changed(event):
    lvShow.configure(text=get_lv())
    
def get_uh():
    return '{:.0f}'.format(u_h.get())

def uh_changed(event):
    uhShow.configure(text=get_uh())

def get_us():
    return '{:.0f}'.format(u_s.get())

def us_changed(event):
    usShow.configure(text=get_us())

def get_uv():
    return '{:.0f}'.format(u_v.get())

def uv_changed(event):
    uvShow.configure(text=get_uv())


sliderFrame = LabelFrame(text='HSV Range Adjustment')
sliderFrame.place(x=185,y=425)

lhLabel = Label(sliderFrame,text='Lower Hue:')
lhLabel.grid(row=0,column=0)
lhSlider = Scale(sliderFrame,orient='horizontal',from_=0,to=179,command=lh_changed,variable=l_h)
lhSlider.grid(row=0,column=1)

lsLabel = Label(sliderFrame,text='Lower Saturation:')
lsLabel.grid(row=0,column=3)
lsSlider = Scale(sliderFrame,orient='horizontal',from_=0,to=255,command=ls_changed,variable=l_s)
lsSlider.grid(row=0,column=4)

lvLabel = Label(sliderFrame,text='Lower Value:')
lvLabel.grid(row=0,column=5)
lvSlider = Scale(sliderFrame,orient='horizontal',from_=0,to=255,command=lv_changed,variable=l_v)
lvSlider.grid(row=0,column=6)

uhLabel = Label(sliderFrame,text='Upper Hue:')
uhLabel.grid(row=1,column=0)
uhSlider = Scale(sliderFrame,orient='horizontal',from_=0,to=179,command=uh_changed,variable=u_h)
uhSlider.grid(row=1,column=1)

usLabel = Label(sliderFrame,text='Upper Saturation:')
usLabel.grid(row=1,column=3)
usSlider = Scale(sliderFrame,orient='horizontal',from_=0,to=255,command=us_changed,variable=u_s)
usSlider.grid(row=1,column=4)

uvLabel = Label(sliderFrame,text='Upper Value:')
uvLabel.grid(row=1,column=5)
uvSlider = Scale(sliderFrame,orient='horizontal',from_=0,to=255,command=uv_changed,variable=u_v)
uvSlider.grid(row=1,column=6)

# ---Result ---
resultFrame = LabelFrame(text='Get Result')
resultFrame.place(x=745,y=425)

lrLabel = Label(resultFrame,text='HSV Lower Range')
lrLabel.grid(row=0,column=0,columnspan=3)

lhShow = Label(resultFrame,text='0')
lhShow.grid(row=1,column=0)
lsShow = Label(resultFrame,text='0')
lsShow.grid(row=1,column=1)
lvShow = Label(resultFrame,text='0')
lvShow.grid(row=1,column=2)

urLabel = Label(resultFrame,text='HSV Upper Range')
urLabel.grid(row=2,column=0,columnspan=3)

uhShow = Label(resultFrame,text='0')
uhShow.grid(row=3,column=0)
usShow = Label(resultFrame,text='0')
usShow.grid(row=3,column=1)
uvShow = Label(resultFrame,text='0')
uvShow.grid(row=3,column=2)

cpyupperBtn = Button(resultFrame,text='Copy',command=get_lowerRange)
cpyupperBtn.grid(row=0,column=3,rowspan=3)

cpylowwerBtn = Button(resultFrame,text='Copy',command=get_upperRange)
cpylowwerBtn.grid(row=3,column=3,rowspan=3)

# Create a OpenCV video capture object
cap = cv2.VideoCapture(camIndex)

# Start updating the frame
update_frame()

# Run the Tkinter event loop
window.mainloop()
cap.release()

