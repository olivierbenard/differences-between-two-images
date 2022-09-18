"""
Module containing a couple of re-used functions.
"""
import os
import pathlib
import numpy as np
import cv2
from dynaconf import settings
from skimage.metrics import structural_similarity as ssim
from differences_between_two_images import logging


logger = logging.getLogger(__name__)


def is_enough_images(images: list) -> bool:
    """
    Take a list of images to compared and check if the cardinality makes sense.
    Args:
        images (list): the paths pointing at the different images.
    Returns:
        bool: True if images can be compared, False otherwise.

    is_enough_images(['dataset/image-1.jpg', 'dataset/image-2.jpg'])
    >>> True

    is_enough_images(['dataset/image-1.jpg'])
    >>> False
    """
    nb_args = len(images)
    if nb_args >= 2:
        return True
    logger.error(
        "You need to provide at least 2 images. %s image(s) provided.", nb_args
    )
    return False


def extract_filename_from_path(path: str) -> str:
    """
    Retrieve the filename from the path.

    Args:
        path (string): the path containing the filename.
    Returns:
        string: the filename.

    extract_filename_from_path('my/random/path/image.png')
    >>> image
    """
    filename = pathlib.Path(path).stem
    logger.debug("Extracted name: %s", filename)
    return filename


def is_image(path: str) -> bool:
    """
    Check if the path point toward an image.

    Args:
        path (string): the image's path.
    Returns:
        bool: True if yes, False otherwise.

    is_image('my_image.png')
    >>> True

    is_image('my_image.html')
    >>> False
    """
    extensions = pathlib.Path(path).suffix
    logging.debug(f"Extracted extension from {path}: {extensions}")
    if extensions in {".png", ".jpg"}:
        return True
    return False


def extract_matrix_from_image(path: str) -> np.ndarray:
    """
    Read the image from the path and return its matrix representation.
    Args:
        path (string): path toward the image.
    Returns:
        np.ndarray: image's matrix representation.
    """
    matrix = cv2.imread(path)
    return matrix


def convert_to_grayscale(frame: np.ndarray) -> np.ndarray:
    """
    Convert image from 3 RGB to 1 gray scale channel.
    Args:
        frame (np.ndarray): the colorized image to convert.
    Returns:
        np.ndarray: the gray-scale image.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return gray


def compute_ssim(image_1: np.ndarray, image_2: np.ndarray) -> tuple[float, np.ndarray]:
    """
    Find the discrepencies between two gray-scale images.
    Args:
        image_1 (np.ndarray): gray-scaled image.
        image_2 (np.ndarray): gray-scaled image.
    Returns:
        score, diff (float, np.ndarray): tuple.
    """
    (score, diff) = ssim(image_1, image_2, full=True)
    return score, diff


def convert_image_to_8bit(image: np.ndarray) -> np.ndarray:
    """
    Convert the image to a 8-bit unsigned integers array
    in the [0,255] range.

    Args:
        image (np.ndarray): the gray-scale image to convert.
    Returns:
        np.ndarray: the converted image.
    """
    return (image * 255).astype("uint8")


def binarize(image: np.ndarray) -> np.ndarray:
    """
    Binarize the given image.
    The returned image contains 3 colors: 0, 127 and 255.
    Args:
        image (np.ndarray): image to binarize.
    Returns:
        np.ndarray: the image to binarize.
    """
    _, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
    return thresh


def find_contours(threshold: np.ndarray) -> tuple:
    """
    Returns a tuple of matrix.
    Each matrice contains the coordinates of a black area.
    Args:
        threshold (np.ndarray): the 3-colors binarized image.
    Returns:
        tuple[np.ndarray]
    """
    contours, _ = cv2.findContours(
        threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    return contours


def bound_contour(image: np.ndarray, contour: np.ndarray) -> None:
    """
    Bound the given contour in the specified image.
    Args:
        image (np.ndarray): the image where to draw the contour.
        contour (np.ndarray): the contour's coordinates.
    Returns:
        None
    """
    x_coordinate, y_coordinate, width, high = cv2.boundingRect(contour)
    cv2.rectangle(
        image,
        (x_coordinate, y_coordinate),
        (x_coordinate + width, y_coordinate + high),
        (36, 255, 12),
        2,
    )


def fill_contour(image: np.ndarray, contour: np.ndarray) -> None:
    """
    Fill the given contour in the specified image.
    Args:
        image (np.ndarray): the image where to draw the contour.
        contour (np.ndarray): the contour's coordinates.
    Returns:
        None
    """
    cv2.drawContours(image, [contour], 0, (0, 255, 0), -1)


def imgsave(filename: str, image: np.ndarray) -> None:
    """
    Save the image under the specified folder and filename.
    Args:
        filename (string): the filename.
        image (np.ndarray): the image.
    Returns:
        None
    """
    path = os.path.join(settings.PATH_RESULTS, filename)
    cv2.imwrite(path, image)


if __name__ == "__main__":
    pass
