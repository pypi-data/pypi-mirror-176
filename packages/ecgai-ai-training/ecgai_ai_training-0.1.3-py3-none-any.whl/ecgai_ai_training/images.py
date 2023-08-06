from pathlib import Path

from numpy import ndarray
from skimage import img_as_ubyte, util
from skimage.filters import threshold_isodata
from skimage.io import imread, imsave
from skimage.util import random_noise


def load_image(image_path: Path, as_gray: bool = False) -> ndarray:
    image = imread(fname=str(image_path), as_gray=as_gray)
    return image


def save_image_as_ubyte(image: ndarray, image_path: Path):
    byte_image = img_as_ubyte(image)
    save_image(image=byte_image, image_path=image_path)


def save_image(image: ndarray, image_path: Path):
    # file_name = os.path.join(save_path, image_name)
    imsave(fname=str(image_path), arr=image)


def create_binary_image(image_path: Path) -> ndarray:
    image = load_image(image_path=image_path, as_gray=True)
    thresh = threshold_isodata(image)
    binary_image = image > thresh
    return binary_image


#
# def create_bool_image(image: ndarray):
#     bool_image = img_as_bool(image=image)
#     return bool_image


def invert_image(image: ndarray):
    inverted_image = util.invert(image)
    return inverted_image


def add_salt_and_pepper_to_image(image: ndarray) -> ndarray:
    noise_image = random_noise(image=image, mode="s&p")
    return noise_image


def add_salt_to_image(image: ndarray) -> ndarray:
    noise_image = random_noise(image=image, mode="salt")
    return noise_image


def add_pepper_to_image(image: ndarray) -> ndarray:
    noise_image = random_noise(image=image, mode="pepper")
    return noise_image
