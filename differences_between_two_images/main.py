import os
import cv2
import click
import keyboard  # or import msvcrt on windows
import numpy as np
from pathlib import Path
import warnings
from dynaconf import settings

warnings.filterwarnings("ignore", category=UserWarning)  # ignore UserWarning
try:
    from skimage.measure import (
        compare_ssim as ssim,
    )  # compare_ssim fully deprecated in version 0.18
except ImportError:
    from skimage.metrics import structural_similarity as ssim


@click.command()
@click.option(
    "-di", "--display-images", is_flag=True, help="Display the images given as an input"
)
@click.option(
    "-dssim",
    "--display-ssim",
    is_flag=True,
    help="Display the computed ssim between reference and images",
)
@click.option(
    "-bd",
    "--bound-differences",
    is_flag=True,
    help="Highlight the differences by bounding them into a rectangle",
)
@click.option(
    "-dd",
    "--draw-differences",
    is_flag=True,
    help="Highlight the differences by drawing them",
)
@click.argument("images", nargs=-1, type=click.Path(exists=True))
def main(display_images, display_ssim, bound_differences, draw_differences, images):
    """
    [IMAGES] = <image of reference> <image(s) to compare with>
    """
    images = list(images)
    num_img = len(images)
    if num_img == 0:
        print("Images files must be specified")
        return
    if num_img < 2:
        print("Image of reference must be compared with, at least, one another image")
        return

    initialized = False
    ref_name = None
    ref_frame = None
    ref_gray_frame = None

    for image in images:

        filename = Path(image).stem  # extract filename from path
        frame = cv2.imread(image)  # extract the np.matrix
        gray = cv2.cvtColor(
            frame, cv2.COLOR_BGR2GRAY
        )  # gray scale (from 3 RGB to 1 gray scale channel)

        if display_images:  # display the input images
            cv2.imshow(filename, frame)

        if not initialized:  # initialisation with the first image
            print(f"{filename} taken as reference")
            ref_name = filename
            ref_frame = frame
            ref_gray_frame = gray
            initialized = True
        else:
            # quantitative approach to determine the exact discrepancies between images
            # using the Structural Similarity Index (SSIM) - cf. ./ressources/

            (score, diff) = ssim(
                ref_gray_frame, gray, full=True
            )  # compute ssim between two images
            print(f"Similarity between {ref_name} and {filename}:", score)

            if display_ssim:
                cv2.imshow(f"difference-between-{ref_name}-and-{filename}", diff)

            diff = (diff * 255).astype(
                "uint8"
            )  # to detect contours, must be converted to  8-bit unsigned integers array in the [0,255] range
            retval, thresh = cv2.threshold(
                diff, 127, 255, cv2.THRESH_BINARY_INV
            )  # binarize image to find the contours
            contours, hirarchy = cv2.findContours(
                thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            temp_ref_frame = ref_frame.copy()
            filled_after = ref_frame.copy()
            mask = np.zeros(temp_ref_frame.shape, dtype="uint8")

            for contour in contours:  # adding a bounding box around the differences
                area = cv2.contourArea(contour)
                if area > 40:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(
                        temp_ref_frame, (x, y), (x + w, y + h), (36, 255, 12), 2
                    )
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (36, 255, 12), 2)
                    cv2.drawContours(mask, [contour], 0, (0, 255, 0), -1)
                    cv2.drawContours(filled_after, [contour], 0, (0, 255, 0), -1)

            if bound_differences:
                cv2.imshow(
                    f"bound-differences-between-{ref_name}-and-{filename}-on-{ref_name}",
                    temp_ref_frame,
                )  # display the image on screen
                cv2.imwrite(
                    os.path.join(
                        settings.PATH_RESULTS,
                        f"bound-differences-between-{ref_name}-and-{filename}-on-{filename}.jpg",
                    ),
                    frame,
                )  # display the image on screen
            if draw_differences:
                cv2.imwrite(
                    os.path.join(
                        settings.PATH_RESULTS,
                        f"draw-differences-between-{ref_name}-and-{filename}.jpg",
                    ),
                    filled_after,
                )  # display the image on screen

    # while True:

    #     keypress = cv2.waitKey(1)

    #     if keypress == 27 or keyboard.is_pressed("q"):
    #         break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
