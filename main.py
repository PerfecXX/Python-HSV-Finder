# Import necessary libraries
import cv2
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np
import pyperclip

# Author and version information
__author__ = "Teeraphat Kullanankanjana"
__version__ = "0.1.0"

# Define the main class for the HSV Range Finder application
class HSVRangeFinder:
    def __init__(self):
        # Initialize camera index and flip options
        self.camIndex = 0
        self.flip_horizontal = False
        self.flip_vertical = False

        # Create the main tkinter window
        self.window = Tk()
        self.window.geometry('910x600')
        self.window.title('HSV Range Finder')
        self.window.resizable(0, 0)
        
        # Initialize video capture using OpenCV
        self.cap = cv2.VideoCapture(self.camIndex)

        # --- Camera Frames ---
        
        # Create a frame for the main camera feed
        self.mainCameraFrame = LabelFrame(self.window, text='Main Camera')
        self.mainCameraFrame.place(x=0, y=0)

        # Create a label to display the video feed
        self.vidLabel1 = Label(self.mainCameraFrame)
        self.vidLabel1.configure(width=300, height=400)
        self.vidLabel1.pack()

        # Create a frame for the result camera feed
        self.contourCameraFrame = LabelFrame(self.window, text='Result Camera')
        self.contourCameraFrame.place(x=305, y=0)

        # Create a label to display the filtered video feed
        self.vidLabel2 = Label(self.contourCameraFrame)
        self.vidLabel2.configure(width=300, height=400)
        self.vidLabel2.pack()

        # Create a frame for the binary mask
        self.outCameraFrame = LabelFrame(self.window, text='Binary Mask')
        self.outCameraFrame.place(x=600, y=0)

        # Create a label to display the binary mask
        self.vidLabel3 = Label(self.outCameraFrame)
        self.vidLabel3.configure(width=300, height=400)
        self.vidLabel3.pack()

        # --- Camera Control Frame ---
        self.cameraControlFrame = LabelFrame(self.window, text='Camera Control')
        self.cameraControlFrame.place(x=0, y=425)

        # Label to display the current camera channel
        self.camChLabel = Label(self.cameraControlFrame, text='CH:0', font=('', 25, 'bold'))
        self.camChLabel.grid(row=0, column=0, columnspan=2)

        # Buttons for camera control
        self.nextCambtn = Button(self.cameraControlFrame, text='Prev Camera', command=self.prev_cam)
        self.nextCambtn.grid(row=1, column=0)
        self.prevCambtn = Button(self.cameraControlFrame, text='Next Camera', command=self.next_cam)
        self.prevCambtn.grid(row=1, column=1)
        self.flipHCambtn = Button(self.cameraControlFrame, text='Flip Horizontal', command=self.flip_horizontal)
        self.flipHCambtn.grid(row=2, column=0)
        self.flipVCambtn = Button(self.cameraControlFrame, text='Flip Vertical', command=self.flip_vertical)
        self.flipVCambtn.grid(row=2, column=1)

        # --- Slider Section ---

        # Initialize slider variables for HSV range adjustment
        self.l_h, self.l_s, self.l_v = DoubleVar(), DoubleVar(), DoubleVar()
        self.u_h, self.u_s, self.u_v = DoubleVar(), DoubleVar(), DoubleVar()

        # Set default values for upper bound sliders
        self.u_h.set(179)
        self.u_s.set(255)
        self.u_v.set(255)

        # Functions to get slider values and update labels
        def get_lh():
            return '{:.0f}'.format(self.l_h.get())

        def lh_changed(event):
            self.lhShow.configure(text=get_lh())

        def get_ls():
            return '{:.0f}'.format(self.l_s.get())

        def ls_changed(event):
            self.lsShow.configure(text=get_ls())

        def get_lv():
            return '{:.0f}'.format(self.l_v.get())

        def lv_changed(event):
            self.lvShow.configure(text=get_lv())

        def get_uh():
            return '{:.0f}'.format(self.u_h.get())

        def uh_changed(event):
            self.uhShow.configure(text=get_uh())

        def get_us():
            return '{:.0f}'.format(self.u_s.get())

        def us_changed(event):
            self.usShow.configure(text=get_us())

        def get_uv():
            return '{:.0f}'.format(self.u_v.get())

        def uv_changed(event):
            self.uvShow.configure(text=get_uv())

        # Create a frame for HSV range adjustment sliders
        self.sliderFrame = LabelFrame(self.window, text='HSV Range Adjustment')
        self.sliderFrame.place(x=185, y=425)

        # Labels and sliders for lower and upper HSV range values
        self.lhLabel = Label(self.sliderFrame, text='Lower Hue:')
        self.lhLabel.grid(row=0, column=0)
        self.lhSlider = Scale(self.sliderFrame, orient='horizontal', from_=0, to=179, command=lh_changed, variable=self.l_h)
        self.lhSlider.grid(row=0, column=1)

        self.lsLabel = Label(self.sliderFrame, text='Lower Saturation:')
        self.lsLabel.grid(row=0, column=3)
        self.lsSlider = Scale(self.sliderFrame, orient='horizontal', from_=0, to=255, command=ls_changed, variable=self.l_s)
        self.lsSlider.grid(row=0, column=4)

        self.lvLabel = Label(self.sliderFrame, text='Lower Value:')
        self.lvLabel.grid(row=0, column=5)
        self.lvSlider = Scale(self.sliderFrame, orient='horizontal', from_=0, to=255, command=lv_changed, variable=self.l_v)
        self.lvSlider.grid(row=0, column=6)

        self.uhLabel = Label(self.sliderFrame, text='Upper Hue:')
        self.uhLabel.grid(row=1, column=0)
        self.uhSlider = Scale(self.sliderFrame, orient='horizontal', from_=0, to=179, command=uh_changed, variable=self.u_h)
        self.uhSlider.grid(row=1, column=1)

        self.usLabel = Label(self.sliderFrame, text='Upper Saturation:')
        self.usLabel.grid(row=1, column=3)
        self.usSlider = Scale(self.sliderFrame, orient='horizontal', from_=0, to=255, command=us_changed, variable=self.u_s)
        self.usSlider.grid(row=1, column=4)

        self.uvLabel = Label(self.sliderFrame, text='Upper Value:')
        self.uvLabel.grid(row=1, column=5)
        self.uvSlider = Scale(self.sliderFrame, orient='horizontal', from_=0, to=255, command=uv_changed, variable=self.u_v)
        self.uvSlider.grid(row=1, column=6)

        # Labels to display current slider values
        self.resultFrame = LabelFrame(self.window, text='Get Result')
        self.resultFrame.place(x=745, y=425)

        self.lrLabel = Label(self.resultFrame, text='HSV Lower Range')
        self.lrLabel.grid(row=0, column=0, columnspan=3)

        self.lhShow = Label(self.resultFrame, text='0')
        self.lhShow.grid(row=1, column=0)
        self.lsShow = Label(self.resultFrame, text='0')
        self.lsShow.grid(row=1, column=1)
        self.lvShow = Label(self.resultFrame, text='0')
        self.lvShow.grid(row=1, column=2)

        self.urLabel = Label(self.resultFrame, text='HSV Upper Range')
        self.urLabel.grid(row=2, column=0, columnspan=3)

        self.uhShow = Label(self.resultFrame, text='0')
        self.uhShow.grid(row=3, column=0)
        self.usShow = Label(self.resultFrame, text='0')
        self.usShow.grid(row=3, column=1)
        self.uvShow = Label(self.resultFrame, text='0')
        self.uvShow.grid(row=3, column=2)

        # Buttons to copy the lower and upper HSV range values to clipboard
        self.cpyupperBtn = Button(self.resultFrame, text='Copy', command=self.get_lowerRange)
        self.cpyupperBtn.grid(row=0, column=3, rowspan=3)

        self.cpylowwerBtn = Button(self.resultFrame, text='Copy', command=self.get_upperRange)
        self.cpylowwerBtn.grid(row=3, column=3, rowspan=3)

    # Method to copy the lower HSV range to clipboard
    def get_lowerRange(self):
        lowerRange = '{},{},{}'.format(self.get_lh(), self.get_ls(), self.get_lv())
        pyperclip.copy(lowerRange)

    # Method to copy the upper HSV range to clipboard
    def get_upperRange(self):
        upperRange = '{},{},{}'.format(self.get_uh(), self.get_us(), self.get_uv())
        pyperclip.copy(upperRange)

    # Method to flip the camera feed horizontally
    def flip_horizontal(self):
        self.flip_horizontal = not self.flip_horizontal
        self.flip_vertical = False
    
    # Method to flip the camera feed vertically
    def flip_vertical(self):
        self.flip_vertical = not self.flip_vertical
        self.flip_horizontal = False
        
    # Method to switch to the next camera channel
    def next_cam(self):
        self.camIndex += 1
        self.cap.release()
        self.cap = cv2.VideoCapture(self.camIndex)
        self.camChLabel.config(text='CH:{}'.format(self.camIndex))

    # Method to switch to the previous camera channel
    def prev_cam(self):
        self.camIndex -= 1
        if self.camIndex < 0:
            messagebox.showerror("Error! Camera Channel Limitation!", "No previous camera")
            self.camIndex = 0
        else:
            self.cap.release()
            self.cap = cv2.VideoCapture(self.camIndex)
            self.camChLabel.config(text='CH:{}'.format(self.camIndex))

    # Method to update the video frame and apply HSV range filtering
    def update_frame(self):
        # Read a frame from the video capture
        ret, frame = self.cap.read()
        if self.flip_horizontal:
            frame = cv2.flip(frame, 1)  # Horizontal mirror
        elif self.flip_vertical:
            frame = cv2.flip(frame, 0)  # Vertical flip
        
        # Get the lower and upper bound values from the sliders
        lower_bound = np.array([self.l_h.get(), self.l_s.get(), self.l_v.get()])
        upper_bound = np.array([self.u_h.get(), self.u_s.get(), self.u_v.get()])

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
        self.vidLabel1.config(image=img1)
        self.vidLabel1.image = img1

        # Update the label's image with the filtered frame
        self.vidLabel2.config(image=img2)
        self.vidLabel2.image = img2

        self.vidLabel3.config(image=img3)
        self.vidLabel3.image = img3

        # Schedule the next frame update
        self.window.after(10, self.update_frame)

    # Getter method to format lower hue value
    def get_lh(self):
        return '{:.0f}'.format(self.l_h.get())

    # Event handler for lower hue slider change
    def lh_changed(self, event):
        self.lhShow.configure(text=self.get_lh())

    # Getter method to format lower saturation value
    def get_ls(self):
        return '{:.0f}'.format(self.l_s.get())

    # Event handler for lower saturation slider change
    def ls_changed(self, event):
        self.lsShow.configure(text=self.get_ls())

    # Getter method to format lower value value
    def get_lv(self):
        return '{:.0f}'.format(self.l_v.get())

    # Event handler for lower value slider change
    def lv_changed(self, event):
        self.lvShow.configure(text=self.get_lv())

    # Getter method to format upper hue value
    def get_uh(self):
        return '{:.0f}'.format(self.u_h.get())

    # Event handler for upper hue slider change
    def uh_changed(self, event):
        self.uhShow.configure(text=self.get_uh())

    # Getter method to format upper saturation value
    def get_us(self):
        return '{:.0f}'.format(self.u_s.get())

    # Event handler for upper saturation slider change
    def us_changed(self, event):
        self.usShow.configure(text=self.get_us())

    # Getter method to format upper value value
    def get_uv(self):
        return '{:.0f}'.format(self.u_v.get())

    # Event handler for upper value slider change
    def uv_changed(self, event):
        self.uvShow.configure(text=self.get_uv())
    
    # Method to release resources and close the application
    def cleanup(self):
        self.cap.release()
        self.window.destroy()
        self.window.after_cancel(self.update_frame)

    # Method to start the application
    def run(self):
        # Create an OpenCV video capture object
        self.cap = cv2.VideoCapture(self.camIndex)

        # Start updating the frame
        self.update_frame()
        
        # Bind the cleanup method to the window's close event
        self.window.protocol("WM_DELETE_WINDOW", self.cleanup)
        
        # Run the Tkinter event loop
        self.window.mainloop()
        self.window.after_cancel(self.update_frame)
        self.cap.release()
