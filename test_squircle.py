import squircle
from PIL import Image
import numpy as np
from pathlib import Path
import pytest
from collections.abc import Iterable
from numbers import Number


TEST_IMAGE_PATH = Path("test_images")
if not TEST_IMAGE_PATH.is_dir():
    raise SystemExit("ERROR: Couldn't find the directory containing the test images")
SQUARE_IMAGE = TEST_IMAGE_PATH / "square_grid.png"
CIRCLE_IMAGE = TEST_IMAGE_PATH / "circle.png"


def _convert_image_data_to_array(image):
    # https://stackoverflow.com/questions/1109422/getting-list-of-pixel-values-from-pil
    pixels = list(image.getdata())
    width, height = image.size
    pixels = [pixels[i * width : (i + 1) * width] for i in range(height)]
    return pixels


def _read_image(image_path, grayscale=False, use_numpy=False):
    image = Image.open(image_path).convert("RGB")
    if grayscale:
        image = image.convert("L")
    if use_numpy:
        return np.asarray(image)
    return _convert_image_data_to_array(image)


def all_pixels_have_the_same_shape_as_the_first_pixel(array):
    first_pixel = array[0][0]
    for row_index, row in enumerate(array):
        for pixel_index, pixel in enumerate(row):
            if not isinstance(pixel, Number):
                assert len(pixel) == len(first_pixel)
            else:
                assert type(pixel) is type(first_pixel)


def sum_pixel_differences(first_image, second_image):
    if isinstance(first_image, np.ndarray) and isinstance(second_image, np.ndarray):
        return np.sum(np.abs(first_image - second_image))

    total_difference = 0
    for first_row, second_row in zip(first_image, second_image):
        for first_pixel, second_pixel in zip(first_row, second_row):
            # turn black and white pixels into gray colored RGB lists
            if isinstance(first_pixel, Number) and isinstance(second_pixel, Number):
                # multiply by 3 so that images with RGB channels have comparable error
                # values to gray scale images
                total_difference += abs(first_pixel - second_pixel) * 3
            else:
                total_difference += sum(
                    abs(x - y) for x, y in zip(first_pixel, second_pixel)
                )
    return total_difference


def test_dimensions_remain_the_same():
    square = _read_image(SQUARE_IMAGE)
    old_height = len(square)
    old_width = len(square[0])

    circle = squircle.to_circle(square)

    assert old_height == len(circle)
    assert old_width == len(circle[0])


def test_mismatched_height_and_width_errors_out():
    square = _read_image(SQUARE_IMAGE)
    rectangle = np.vstack((square, square))
    with pytest.raises(ValueError):
        squircle.to_circle(rectangle)


@pytest.mark.parametrize("filename", [SQUARE_IMAGE, CIRCLE_IMAGE])
@pytest.mark.parametrize("grayscale", (False, True))
@pytest.mark.parametrize("use_numpy", (False, True))
@pytest.mark.parametrize("method_name", squircle.methods)
def test_convert_then_back_and_compare(filename, grayscale, use_numpy, method_name):
    original = _read_image(filename, grayscale, use_numpy)

    is_circle = filename == CIRCLE_IMAGE
    if is_circle:
        converted = squircle.to_square(original, method_name)
        back_to_original = squircle.to_circle(converted, method_name)
    else:
        converted = squircle.to_circle(original, method_name)
        back_to_original = squircle.to_square(converted, method_name)

    assert len(original) == len(back_to_original)
    assert len(original[0]) == len(back_to_original[0])

    if use_numpy:
        print(grayscale, original.shape)
        assert not np.any(np.isnan(converted))
        assert not np.any(np.isinf(converted))
        assert not np.any(np.isnan(back_to_original))
        assert not np.any(np.isinf(back_to_original))

    for image in [original, converted, back_to_original]:
        all_pixels_have_the_same_shape_as_the_first_pixel(image)

    # TODO: toggle this with a command line argument to pytest
    # from matplotlib import pyplot as plt
    # plt.subplot(1, 3, 1)
    # plt.imshow(original)
    # plt.subplot(1, 3, 2)
    # plt.imshow(np.array(converted))
    # plt.subplot(1, 3, 3)
    # plt.imshow(back_to_original)
    # title = method_name + (" (with numpy)" if use_numpy else "")
    # plt.suptitle(title)
    # plt.show()

    total_difference = sum_pixel_differences(original, back_to_original)
    average_difference = total_difference / (len(original) * len(original))
    # TODO: this is too high
    assert average_difference < 400
