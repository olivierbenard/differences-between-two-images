"""
Module to pinpoint the difference between images.
"""

import logging
import cv2
import click
import numpy as np
from differences_between_two_images.helpers import utils
from differences_between_two_images.helpers import exceptions

logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "-ds",
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
@click.option(
    "-dm",
    "--draw-mask",
    is_flag=True,
    type=bool,
    default=False,
    help="Highlight the mask by drawing them",
)
@click.argument("images", nargs=-1, type=click.Path(exists=True))
def main(  # pylint: disable=too-many-locals
    display_ssim: bool,
    bound_differences: bool,
    draw_differences: bool,
    draw_mask: bool,
    images: list[str],
) -> None:
    """
    Highlight the difference bewteen the provided images.
    Args:
        display_ssim (bool): flag to save the binarized differences.
        bound_differences (bool): flag to circle the differences and save the result.
        draw_differences (bool): flag to draw the differences and save the result.
        draw_mask (bool): flag to draw the mask from the difference and save the result.
        images (list): list of images to compared.
    Returns:
        None
    """
    images = list(images)
    logger.info("Retrieved the following images: %s", images)

    if not utils.is_enough_images(images):
        raise exceptions.NotEnoughArgumentsException()

    reference_path = images[0]
    reference_name = utils.extract_filename_from_path(reference_path)
    reference_frame = utils.extract_matrix_from_image(reference_path)
    reference_frame_gray = utils.convert_to_grayscale(reference_frame)

    for image in images[1:]:

        name = utils.extract_filename_from_path(image)
        frame = utils.extract_matrix_from_image(image)
        frame_gray = utils.convert_to_grayscale(frame)

        (score, diff) = utils.compute_ssim(reference_frame_gray, frame_gray)
        logging.info("Similarity between %s and %s: %s", reference_name, name, score)

        diff = utils.convert_image_to_8bit(diff)
        thresh = utils.binarize(diff)

        if display_ssim:
            utils.imgsave(f"difference-between-{reference_name}-and-{name}.jpg", thresh)

        contours = utils.find_contours(thresh.copy())

        frame_filled_after = reference_frame.copy()
        mask = np.zeros(frame_filled_after.shape, dtype="uint8")

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 40:
                # add a bounding box around the difference
                utils.bound_contour(reference_frame, contour)
                utils.bound_contour(frame, contour)
                # draw over the difference
                utils.fill_contour(mask, contour)
                utils.fill_contour(frame_filled_after, contour)

        if draw_mask:
            utils.imgsave(f"mask-between-{reference_name}-and-{name}.jpg", mask)
        if bound_differences:
            utils.imgsave(
                f"bound-differences-between-{reference_name}-and-{name}-on-{name}.jpg",
                frame,
            )
        if draw_differences:
            utils.imgsave(
                f"draw-differences-between-{reference_name}-and-{name}-on-{name}.jpg",
                frame_filled_after,
            )

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
