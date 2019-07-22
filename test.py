import squircle
from PIL import Image
import numpy as np
import math
from pathlib import Path
import pytest


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


def read_image(image_path):
    return np.asarray(Image.open(square_image))


def test_dimensions_remain_the_same():
    square = read_image(square_image)
    old_height = len(square)
    old_width = len(square[0])

    disc = squircle.to_disk(square)

    assert old_height == len(disc)
    assert old_width == len(disc[0])


def test_mismatched_height_and_width_errors_out():
    with pytest.raises(ValueError):
        square = read_image(square_image)
        rectangle = np.vstack((square, square))

        squircle.to_disk(rectangle)


@pytest.mark.parametrize("method_name", squircle.methods)
def test_method(method_name):
    square = read_image(square_image)

    disk = squircle.to_disk(square, method_name)
    back_to_square = squircle.to_disk(square, method_name)

    assert len(square) == len(back_to_square)
    assert len(square[0]) == len(back_to_square[0])

    total_difference = np.sum(square - back_to_square)
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

