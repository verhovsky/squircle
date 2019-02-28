import squircle
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


def test_method(method_name, filename="test/retina.jpg"):
    circle = np.asarray(Image.open(filename))

    square = squircle.to_square(circle, method_name)

    plt.imshow(square)
    plt.title = "Circular image converted to square"
    plt.show()

    circle_back = squircle.to_disk(square, method_name)

    plt.imshow(circle_back)
    plt.title = "Square image converted back to circle"
    plt.show()


for method in squircle.methods:
    test_method(method)

# test_method("simple_stretch")
