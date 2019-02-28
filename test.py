import squircle
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


circle = np.asarray(Image.open("test/retina.jpg"))

square = squircle.to_square(circle)

plt.imshow(square)
plt.title = "Circular image converted to square"
plt.show()

circle_back = squircle.to_disk(square)

plt.imshow(circle_back)
plt.title = "Square image converted back to circle"
plt.show()
