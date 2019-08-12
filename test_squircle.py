import squircle
from PIL import Image
import numpy as np
import math
from pathlib import Path
import pytest
import itertools
from matplotlib import pyplot as plt


square_image = Path("test_images/square_grid.png")


def _convert_image_data_to_array(image):
    # https://stackoverflow.com/questions/1109422/getting-list-of-pixel-values-from-pil
    pixels = list(image.getdata())
    width, height = image.size
    pixels = [pixels[i * width : (i + 1) * width] for i in range(height)]
    return pixels


def read_image(image_path, use_numpy=False):
    image = Image.open(square_image)
    if use_numpy:
        return np.asarray(image)
    return _convert_image_data_to_array(image)
    return image


def test_dimensions_remain_the_same():
    square = read_image(square_image)
    old_height = len(square)
    old_width = len(square[0])

    circle = squircle.to_circle(square)

    assert old_height == len(circle)
    assert old_width == len(circle[0])


def test_mismatched_height_and_width_errors_out():
    square = read_image(square_image)
    rectangle = np.vstack((square, square))
    with pytest.raises(ValueError):
        squircle.to_circle(rectangle)


@pytest.mark.parametrize("filename", (square_image,))
@pytest.mark.parametrize("method_name", squircle.methods)
@pytest.mark.parametrize("use_numpy", (True, False))
def test_method(filename, method_name, use_numpy):
    square = read_image(filename, use_numpy)

    circle = squircle.to_circle(square, method_name)
    back_to_square = squircle.to_square(square, method_name)

    assert len(square) == len(back_to_square)
    assert len(square[0]) == len(back_to_square[0])

    assert not np.any(np.isnan(circle))
    assert not np.any(np.isinf(circle))
    assert not np.any(np.isnan(back_to_square))
    assert not np.any(np.isinf(back_to_square))

    total_difference = 0
    if use_numpy:
        total_difference = np.sum(np.abs(square - back_to_square))
    else:
        for square_row, back_to_square_row in zip(square, back_to_square):
            for x, y in zip(square_row, back_to_square_row):
                total_difference += abs(x - y)

    average_difference = total_difference / (len(square) * len(square))
    # TODO: this is too high
    assert average_difference < 30

    # TODO: how do I pass a command line argument to a parametrized test?
    # plt.subplot(1, 3, 1)
    # plt.imshow(square)
    # plt.subplot(1, 3, 2)
    # plt.imshow(circle)
    # plt.subplot(1, 3, 3)
    # plt.imshow(back_to_square)
    # plt.show()

