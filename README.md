[`squircle.py`](https://pypi.org/project/squircle/) is a Python utility for
stretching circles into squares and squishing squares into circles. It requires
Python 3.6 or later.

## Installation

```sh
pip install squircle
```

## Usage:

```python
import numpy as np
from PIL import Image

from squircle import to_circle, to_square

square = np.asarray(Image.open('some-square-image.jpg'))
circle = to_circle(square)
and_back_to_square = to_square(circle)
```

there's 3 stretching methods you can choose from

```python
>>> from squircle import methods
>>> list(methods.keys())
['fgs', 'stretch', 'elliptical']
>>> circle = to_circle(square, method='elliptical')
```

### Stretching methods

#### Fernández-Guasti squircle (`fgs`)

The Fernández-Guasti squircle is used by default.

https://squircular.blogspot.com/2015/09/fernandez-guastis-squircle.html

http://mathworld.wolfram.com/Squircle.html

#### Simple Stretching (`stretch`)

This method "just linearly stretches each point radially so that the rim of the circle matches the rim of the square".

https://squircular.blogspot.com/2015/09/elliptical-arc-mapping.html

#### Elliptical grid mapping (`elliptical`)

"The way I went about this was to think of a line of constant x (as well as a line of constant y) getting mapped to an ellipse in the circle"

https://mathproofs.blogspot.com/2005/07/mapping-square-to-circle.html

https://squircular.blogspot.com/2015/09/mapping-circle-to-square.html

#### Schwarz-Christoffel conformal mapping

`raise NotImplementedError`. The math is difficult.

https://squircular.blogspot.com/2015/09/schwarz-christoffel-mapping.html

http://jcgt.org/published/0005/02/01/

## Development

After `pip install tox` you can run squircle's (limited) test set with

```sh
tox
```

On Ubuntu, you also need the following dependencies for numpy and matplotlib

```sh
sudo apt install python3-dev libjpeg-dev zlib1g-dev libfreetype6-dev
```

You can visually inspect the transformations by uncommenting the matplotlib code in `test_squircle.py` and then invoking the tests directly with `pytest` instead of tox

``` sh
pytest
```

but you'll need to install the dependencies of the tests manually, which you can do with `pip install pytest numpy matplotlib pillow`.

## TODOs

If you would like to help with this project, [the open issues on GitHub](https://github.com/verhovsky/squircle/issues) should list some ideas.

## Credits

This code is converted from the C++ sources on Chamberlain Fong's blog posts, which (I think) are based on his paper [Analytical Methods for Squaring the Disc (2014)](https://arxiv.org/ftp/arxiv/papers/1509/1509.06344.pdf).

The square image in `test_images/` is https://commons.wikimedia.org/wiki/File:Graph-paper.svg and the circle is taken from Chamberlain Fong's blog posts.
