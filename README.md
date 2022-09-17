# differences-between-two-images (or multiple images)
Detect and visualize differences between images with `OpenCV` and the SSIM method. The images are compared with the first provided image.

## Dependencies

To manage the dependencies, I recommend using the python package manager `poetry`. You might have to install it before using `brew install poetry` (on MacOS).

Then, just install the different dependencies:

    poetry update

**Note:** In case you want to use any other methods, a `requirements.txt` file is also provided.

## Quick-start

Once the virtual environment is set up, you can call the script using different parameters.

On MacOS:

    poetry run main $(ls ./dataset/*.jpg)

On Windows PowerShell:

    python ./main.py $(dir ./dataset/*.jpg)

You can also add options to display:
- The input images `-di` (display images)
- The boxed differences `-db` (display bounds)
- The drawed differences `-dd` (draw differences)
- The computed ssim model `-dssim` (display ssim)

**Note:** the first given file is the reference which will be use for comparison.

### Example

    python ./main.py image-1.jpg image-2.jpg image-3.jpg

`image-2.jpg` and `image-3.jpg` will be compared to `image-1.jpg`.

## Inspirations
- https://stackoverflow.com/questions/56183201/detect-and-visualize-differences-between-two-images-with-opencv-python
- https://ece.uwaterloo.ca/~z70wang/publications/ssim.pdf
