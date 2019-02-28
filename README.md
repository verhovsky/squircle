`squircle.py` is a Python 3 utility for stretching discs/circles into squares and squishing squares into discs/circles

### Usage:

```python
from squircle import to_disc, to_square
from PIL import Image

square = np.asarray(Image.open('some-square-image.jpg'))
disc = to_disc(square)
and_back_to_square = to_square(disc)
```

there's 3 stretching methods you can choose from

```python
>>> from squircle import methods
>>> list(methods.keys())
['fgs', 'simple_stretch', 'elliptical']
>>> disc = to_disc(square, method='elliptical')
```

The Fernández-Guasti squircle (`fgs`) is used by default

#### read

[Analytical Methods for Squaring the Disc by C Fong 2014](https://arxiv.org/ftp/arxiv/papers/1509/1509.06344.pdf)

https://squircular.blogspot.com/2015/09/schwarz-christoffel-mapping.html

https://squircular.blogspot.com/2015/09/fernandez-guastis-squircle.html

http://mathworld.wolfram.com/Squircle.html

[Elliptification of Rectangular Imagery by C Fong - ‎2017](https://arxiv.org/pdf/1709.07875.pdf) (for rectangles and ovals)
