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
['fgs', 'stretch', 'elliptical']
>>> disc = to_disc(square, method='elliptical')
```

#### Stretching methods

##### Fernández-Guasti squircle (`fgs`) 

The Fernández-Guasti squircle (`fgs`) is used by default.

https://squircular.blogspot.com/2015/09/fernandez-guastis-squircle.html

http://mathworld.wolfram.com/Squircle.html

##### Simple Stretching (`stretch`)

This method just linearly stretches each point radially so that the rim of the circle matches the rim of the square.

https://squircular.blogspot.com/2015/09/elliptical-arc-mapping.html

##### Elliptical grid mapping (`elliptical`)

"The way I went about this was to think of a line of constant x (as well as a line of constant y) getting mapped to an ellipse in the circle"

https://mathproofs.blogspot.com/2005/07/mapping-square-to-circle.html

https://squircular.blogspot.com/2015/09/mapping-circle-to-square.html

##### Schwarz-Christoffel conformal mapping

`raise NotImplementedError`. The math is allegedly difficult.

https://squircular.blogspot.com/2015/09/schwarz-christoffel-mapping.html

http://jcgt.org/published/0005/02/01/

---

This code is converted from the C++ sources on Chamberlain Fong's blog posts, which (I think) is based on his paper [Analytical Methods for Squaring the Disc by C Fong 2014](https://arxiv.org/ftp/arxiv/papers/1509/1509.06344.pdf).

Squircle doesn't handle ellipses/rectangles, this more recent paper should be useful: [Elliptification of Rectangular Imagery by C Fong - ‎2017](https://arxiv.org/pdf/1709.07875.pdf)
