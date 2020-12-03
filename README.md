# differences-between-two-images (or multiple images)
Detect and visualize differences between two (or multiple) images with OpenCV Python using SSIM method.

__Librairies needed__
- cv2
- numpy
- click
- keyboard
- scikit-image

Once the virtual environment is set, you can download the required modules using:
`pip install -r requirements.txt`

## Quickstart
`python ./main.py $(dir ./dataset/*.jpg)` on Windows PowerShell

You can also add options to display:
- The input images `-di` (which stands for: display images)
- The boxed differences `-db` (which stands for: display bounds)
- The drawed differences `-dd` (which stands for: draw differences)
- The computed ssim model `-dssim` (which stands for: display ssim)

__Note that the first given file is the reference which will be use for comparison__.

E.g. : 
`python ./main.py image-1.jpg image-2.jpg image-3.jpg`

Image-2 and Image-3 will be compared to Image-1.

## Inspirations
- https://stackoverflow.com/questions/56183201/detect-and-visualize-differences-between-two-images-with-opencv-python
- https://ece.uwaterloo.ca/~z70wang/publications/ssim.pdf

