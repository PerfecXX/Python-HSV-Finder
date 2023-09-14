# Python HSV Range Finder
Using the Tkinter GUI and OpenCV to filter and get the upper and lower HSV ranges from camera video capture

![](https://github.com/PerfecXX/GUI-HSV-Range-Finder/blob/main/doc/doc_filter_red.png)

## Main Feature

1. View Camera Feed: This package captures video from a camera (webcam) and displays it in a GUI window. The camera feed is continuously updated.

2. Adjust HSV Range: This package provides sliders for adjusting the lower and upper bounds of the HSV (Hue, Saturation, Value) color range. These sliders allow you to define a specific color range you want to isolate from the camera feed.

3. View Filtered Result: This package processes the camera feed using the HSV range values set by the sliders. It filters out the colors that fall within the specified range and displays the result in a separate frame.

4. View Binary Mask: This package converts the filtered result into a binary mask, where the isolated color range appears as white, and everything else appears as black. This binary mask is displayed in a third frame.

5. Copy HSV Range Values: This package includes buttons that allow you to copy the current lower and upper HSV range values to the clipboard, making it easy to use these values in other applications.

6. Switch Cameras: You can switch between different cameras if you have multiple camera devices connected to your computer.

## Dependencies

Before running this package, you need to install the following package dependencies:

1. [opencv-contrib-python](https://pypi.org/project/opencv-contrib-python/)
2. [PIL](https://pypi.org/project/Pillow/)
3. [pyperclip](https://pypi.org/project/pyperclip/) 

```python
pip install opencv-contrib-python
```

```python
pip install pillow
```

```python
pip install pyperclip
```
