"""
Module to pinpoint the difference between images.
"""

import warnings
import logging
import cv2
import click
import numpy as np
from differences_between_two_images.helpers import utils

warnings.filterwarnings("ignore", category=UserWarning)  # ignore UserWarning

logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "-di",
    "--display-images",
    is_flag=True,
    type=bool,
    default=False,
    help="Display the images given as an input",
)
@click.option(
    "-dssim",
    "--display-ssim",
    is_flag=True,
    type=bool,
    default=False,
    help="Display the computed ssim between reference and images",
)
@click.option(
    "-bd",
    "--bound-differences",
    is_flag=True,
    type=bool,
    default=False,
    help="Highlight the differences by bounding them into a rectangle",
)
@click.option(
    "-dd",
    "--draw-differences",
    is_flag=True,
    type=bool,
    default=False,
    help="Highlight the differences by drawing them",
)
@click.argument("images", nargs=-1, type=click.Path(exists=True))
def main(
    display_images: bool,
    display_ssim: bool,
    bound_differences: bool,
    draw_differences: bool,
    images: list,
) -> None:
    """
    [IMAGES] = <image of reference> <image(s) to compare with>
    """
    images = list(images)
    logger.info("Retrieved the following images: %s", images)

    if not utils.is_enough_images(images):
        # TODO: raise a custom error
        return

    initialized = False
    ref_name = None
    ref_frame = None
    ref_gray_frame = None

    for image in images:

        filename = utils.extract_filename_from_path(image)  # extract filename from path
        if not utils.is_image(image):
            return
        frame = utils.extract_matrix_from_image(image)  # extract the np.matrix
        gray = utils.convert_to_grayscale(frame)

        if display_images:  # display the input images
            cv2.imshow(filename, frame)

        if not initialized:  # initialisation with the first image
            logger.info("%s will be taken as reference" % (filename))
            ref_name = filename
            ref_frame = frame
            ref_gray_frame = gray
            initialized = True
        else:
            # quantitative approach to determine the exact discrepancies between images
            # using the Structural Similarity Index (SSIM) - cf. ./ressources/
            (score, diff) = utils.compute_ssim(
                ref_gray_frame, gray
            )  # compute ssim between two images
            logging.info(
                "Similarity between %s and %s: %s" % (ref_name, filename, score)
            )

            if display_ssim:
                cv2.imshow(f"difference-between-{ref_name}-and-{filename}", diff)

            diff = utils.convert_image_to_8bit(
                diff
            )  # convert to 8-bit unsigned integers array in the [0,255] range
            utils.imgsave("diff.jpg", diff)
            thresh = utils.binarize(diff)  # binarize image to find the contours
            utils.imgsave("thresh.jpg", diff)
            contours = utils.find_contours(thresh.copy())

            temp_ref_frame = ref_frame.copy()
            filled_after = ref_frame.copy()
            mask = np.zeros(temp_ref_frame.shape, dtype="uint8")

            for contour in contours:  # adding a bounding box around the differences
                area = cv2.contourArea(contour)
                if area > 40:
                    utils.bound_contour(temp_ref_frame, contour)
                    utils.bound_contour(frame, contour)
                    utils.fill_contour(mask, contour)
                    utils.fill_contour(filled_after, contour)

            if bound_differences:
                utils.imgsave(
                    f"bound-differences-between-{ref_name}-and-{filename}-on-{filename}.jpg",
                    frame,
                )  # display the image on screen
            if draw_differences:
                utils.imgsave(
                    f"draw-differences-between-{ref_name}-and-{filename}.jpg",
                    filled_after,
                )  # display the image on screen

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
