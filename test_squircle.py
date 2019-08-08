import squircle
from PIL import Image
import numpy as np
import math
from pathlib import Path
import pytest
import itertools


def pytest_addoption(parser):
    parser.addoption(
        "--visual",
        action="store",
        default="type1",
        help="whether to display the results of conversion using matplotlib",
    )


@pytest.fixture
def visual(request):
    return request.config.getoption("--visual")


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

    disc = squircle.to_disk(square)

    assert old_height == len(disc)
    assert old_width == len(disc[0])


def test_mismatched_height_and_width_errors_out():
    square = read_image(square_image)
    rectangle = np.vstack((square, square))
    with pytest.raises(ValueError):
        squircle.to_disk(rectangle)


@pytest.mark.parametrize("method_name", squircle.methods)
@pytest.mark.parametrize("use_numpy", (True, False))
def test_method(method_name, use_numpy):
    square = read_image(square_image, use_numpy)

    disk = squircle.to_disk(square, method_name)
    back_to_square = squircle.to_disk(square, method_name)

    assert len(square) == len(back_to_square)
    assert len(square[0]) == len(back_to_square[0])

    assert not np.any(np.isnan(disk))
    assert not np.any(np.isinf(disk))
    assert not np.any(np.isnan(back_to_square))
    assert not np.any(np.isinf(back_to_square))

    total_difference = 0
    if use_numpy:
        total_difference = np.sum(np.abs(square - back_to_square))
    else:
        for square_row, back_to_square_row in zip(square, back_to_square):
            for x, y in zip(square_row, back_to_square_row):
                total_difference += abs(x - y)

    # TODO: this is way too high
    assert total_difference < 10000000

    # if visual:
    #     import matplotlib.pyplot as plt

    #     plt.imshow(square)
    #     plt.title = "Circular image converted to square"
    #     plt.show()
    #     plt.imshow(disc)
    #     plt.title = "Circular image converted to square"
    #     plt.show()
    #     plt.imshow(back_to_square)
    #     plt.title = "Circular image converted to square"
    #     plt.show()

