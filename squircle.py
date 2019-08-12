#!/usr/bin/env python3

from math import sqrt as _sqrt, floor as _floor

try:
    import numpy as _np

    _HAS_NUMPY = True
except ImportError:
    _HAS_NUMPY = False

_epsilon = 0.0000000001


def _sgn(x):
    if x == 0.0:
        return 0.0
    if x < 0:
        return -1.0
    return 1.0


# https://squircular.blogspot.com/2015/09/elliptical-arc-mapping.html
def _stretch_square_to_disc(x, y):
    if (abs(x) < _epsilon) or (abs(y) < _epsilon):
        return x, y

    x2 = x * x
    y2 = y * y
    hypotenuse_squared = x * x + y * y

    # code can use fast reciprocal sqrt floating point trick
    # https://en.wikipedia.org/wiki/Fast_inverse_square_root
    reciprocal_hypotenuse = 1.0 / _sqrt(hypotenuse_squared)

    multiplier = 1.0
    # a trick based on Dave Cline's idea
    # if abs(x2) > abs(y2):
    if x2 > y2:
        multiplier = _sgn(x) * x * reciprocal_hypotenuse
    else:
        multiplier = _sgn(y) * y * reciprocal_hypotenuse

    return x * multiplier, y * multiplier


# TODO: goes outside circle bounds in the left and on top
def _stretch_disc_to_square(u, v):
    if (abs(u) < _epsilon) or (abs(v) < _epsilon):
        return u, v

    u2 = u * u
    v2 = v * v
    r = _sqrt(u2 + v2)

    # a trick based on Dave Cline's idea
    # http://psgraphics.blogspot.com/2011/01/improved-code-for-concentric-map.html
    if u2 >= v2:
        sgnu = _sgn(u)
        return sgnu * r, sgnu * r * v / u
    else:
        sgnv = _sgn(v)
        return sgnv * r * u / v, sgnv * r


# https://squircular.blogspot.com/2015/09/fg-squircle-mapping.html
def _fgs_square_to_disc(x, y):
    x2 = x * x
    y2 = y * y
    r2 = x2 + y2
    rad = _sqrt(r2 - x2 * y2)

    # avoid division by zero if (x,y) is close to origin
    if r2 < _epsilon:
        return

    # This code is amenable to the fast reciprocal sqrt floating point trick
    # https://en.wikipedia.org/wiki/Fast_inverse_square_root
    reciprocal_sqrt = 1.0 / _sqrt(r2)

    u = x * rad * reciprocal_sqrt
    v = y * rad * reciprocal_sqrt
    return u, v


def _fgs_disc_to_square(u, v):
    x = u
    y = v

    u2 = u * u
    v2 = v * v
    r2 = u2 + v2

    if r2 > 1:  # we're outside the disc
        return

    uv = u * v
    fouru2v2 = 4.0 * uv * uv
    rad = r2 * (r2 - fouru2v2)
    sgnuv = _sgn(uv)
    sqrto = _sqrt(0.5 * (r2 - _sqrt(rad)))

    if abs(u) > _epsilon:
        y = sgnuv / u * sqrto

    if abs(v) > _epsilon:
        x = sgnuv / v * sqrto

    return x, y


# https://squircular.blogspot.com/2015/09/mapping-circle-to-square.html
def _elliptical_square_to_disc(x, y):
    try:
        return x * _sqrt(1.0 - y * y / 2.0), y * _sqrt(1.0 - x * x / 2.0)
    except ValueError:  # sqrt of a negative number
        return None


# TODO: goes outside original circle in some places
def _elliptical_disc_to_square(u, v):
    u2 = u * u
    v2 = v * v
    twosqrt2 = 2.0 * _sqrt(2.0)
    subtermx = 2.0 + u2 - v2
    subtermy = 2.0 - u2 + v2
    termx1 = subtermx + u * twosqrt2
    termx2 = subtermx - u * twosqrt2
    termy1 = subtermy + v * twosqrt2
    termy2 = subtermy - v * twosqrt2
    try:
        x = 0.5 * _sqrt(termx1) - 0.5 * _sqrt(termx2)
        y = 0.5 * _sqrt(termy1) - 0.5 * _sqrt(termy2)
        return x, y
    except ValueError:  # sqrt of a negative number
        return None


# if the coordinate is an index in an image it's between 0 and the length of the image
# we need it to be between -1 and 1 for the math
def _pixel_coordinates_to_one(coordinate, max_value):
    return coordinate / max_value * 2 - 1


def _one_coordinates_to_pixels(coordinate, max_value):
    return (coordinate + 1) / 2 * max_value


def _check_that_all_sides_are_the_same_length(inp):
    for x, row in enumerate(inp):
        if len(row) != len(inp):
            raise ValueError(
                f"The input image must be square shaped but row {x} "
                f"is {len(row)} pixels accross, while the other side of the "
                f"image is {len(inp)}"
            )


def _transform(inp, coordinate_transformer=_fgs_square_to_disc):
    # TODO: you should be able to extend this to rectangles and ovals
    # Elliptification of Rectangular Imagery by C Fong - ‎2017
    # https://arxiv.org/pdf/1709.07875.pdf
    _check_that_all_sides_are_the_same_length(inp)

    if _HAS_NUMPY and isinstance(inp, _np.ndarray):
        result = _np.zeros_like(inp)
    else:
        result = [[0] * len(inp) for _ in inp]

    for x, row in enumerate(inp):
        # convert pixel coordinates to TODO: what is this called? it's not a unit square
        # x and y are in the range(0, len(inp)) but they need to be between -1 and 1
        # for the code
        unit_x = _pixel_coordinates_to_one(x, len(inp))

        for y, _ in enumerate(row):
            unit_y = _pixel_coordinates_to_one(y, len(row))

            try:
                uv = coordinate_transformer(unit_x, unit_y)
                if uv is None:
                    continue
                u, v = uv

                u = _one_coordinates_to_pixels(u, len(inp))
                v = _one_coordinates_to_pixels(v, len(row))

                # TODO: something smarter than flooring.
                # maybe take a weighted average of the nearest 4 pixels
                result[x][y] = inp[_floor(u)][_floor(v)]
            except IndexError:
                pass

    return result


methods = {
    "fgs": {"to_square": _fgs_disc_to_square, "to_disc": _fgs_square_to_disc},
    "stretch": {
        "to_square": _stretch_disc_to_square,
        "to_disc": _stretch_square_to_disc,
    },
    "elliptical": {
        "to_square": _elliptical_disc_to_square,
        "to_disc": _elliptical_square_to_disc,
    },
    # TODO: Schwarz-Christoffel
    # https://squircular.blogspot.com/2015/09/schwarz-christoffel-mapping.html
}


def to_square(disk, method="fgs"):
    if method not in methods:
        raise ValueError(
            f'"{method}" is not a valid method. '
            f'The choices are {" and ".join(", ".join(methods.keys()).rsplit(", ", 1))}.'
        )
    # using square_to_disc to convert discs to squares is counterintuitive
    return _transform(disk, methods[method]["to_disc"])


def to_circle(square, method="fgs"):
    if method not in methods:
        raise ValueError(
            f'"{method}" is not a valid method. '
            f'The choices are {" and ".join(", ".join(methods.keys()).rsplit(", ", 1))}.'
        )
    # using disc_to_square to convert squares to discs is counterintuitive
    return _transform(square, methods[method]["to_square"])


def to_disk(square, method="fgs"):
    import warnings

    warnings.warn(
        "to_disk has been deprecated due to possible confusion "
        "between the spelling of disc and disk. Please use to_circle() instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return to_circle(square, method)
