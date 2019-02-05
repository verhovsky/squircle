import square2circle
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


circle = np.asarray(Image.open("test/retina.jpg"))
square = square2circle.to_square(circle)
# circle_back = square2circle.simple_square(square)

plt.imshow(square)
plt.show()

circle_back = square2circle.to_circle(square)
plt.imshow(circle_back)
plt.show()
