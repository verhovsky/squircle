#!/usr/bin/env python3

from math import sqrt, floor, ceil
import numpy as np

epsilon = 0.000_000_000_1


def sgn(x):
    if x == 0.0:
        return 0.0
    if x < 0:
        return -1.0
    return 1.0


# https://squircular.blogspot.com/2015/09/fg-squircle-mapping.html
def fgs_square_to_disc(x, y):
    x2 = x * x
    y2 = y * y
    r2 = x2 + y2
    rad = sqrt(r2 - x2 * y2)

    # avoid division by zero if (x,y) is close to origin
    if r2 < epsilon:
        return

    # This code is amenable to the fast reciprocal sqrt floating point trick
    # https://en.wikipedia.org/wiki/Fast_inverse_square_root
    reciprocal_sqrt = 1.0 / sqrt(r2)

    u = x * rad * reciprocal_sqrt
    v = y * rad * reciprocal_sqrt
    return u, v


def fgs_disc_to_square(u, v):
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
    sgnuv = sgn(uv)
    sqrto = sqrt(0.5 * (r2 - sqrt(rad)))

    if abs(u) > epsilon:
        y = sgnuv / u * sqrto

    if abs(v) > epsilon:
        x = sgnuv / v * sqrto

    return x, y


# https://squircular.blogspot.com/2015/09/elliptical-arc-mapping.html
def simple_stretch_disc_to_square(u, v):
    if (abs(u) < epsilon) or (abs(v) < epsilon):
        return u, v

    u2 = u * u
    v2 = v * v
    r = sqrt(u2 + v2)

    # a trick based on Dave Cline's idea
    # link Peter Shirley's blog
    if u2 >= v2:
        sgnu = sgn(u)
        return sgnu * r, sgnu * r * v / u
    else:
        sgnv = sgn(v)
        return sgnv * r * u / v, sgnv * r


def simple_stretch_square_to_disc(x, y):
    if (abs(x) < epsilon) or (abs(y) < epsilon):
        return x, y

    x2 = x * x
    y2 = y * y
    hypotenuse_squared = x * x + y * y

    # code can use fast reciprocal sqrt floating point trick
    # https://en.wikipedia.org/wiki/Fast_inverse_square_root
    reciprocal_hypotenuse = 1.0 / sqrt(hypotenuse_squared)

    multiplier = 1.0
    # a trick based on Dave Cline's idea
    # if abs(x2) > abs(y2):
    if x2 > y2:
        multiplier = sgn(x) * x * reciprocal_hypotenuse
    else:
        multiplier = sgn(y) * y * reciprocal_hypotenuse

    return x * multiplier, y * multiplier


# https://squircular.blogspot.com/2015/09/mapping-circle-to-square.html
def elliptical_disc_to_square(u, v):
    u2 = u * u
    v2 = v * v
    twosqrt2 = 2.0 * sqrt(2.0)
    subtermx = 2.0 + u2 - v2
    subtermy = 2.0 - u2 + v2
    termx1 = subtermx + u * twosqrt2
    termx2 = subtermx - u * twosqrt2
    termy1 = subtermy + v * twosqrt2
    termy2 = subtermy - v * twosqrt2
    x = 0.5 * sqrt(termx1) - 0.5 * sqrt(termx2)
    y = 0.5 * sqrt(termy1) - 0.5 * sqrt(termy2)
    return x, y


def elliptical_square_to_disc(x, y):
    return x * sqrt(1.0 - y * y / 2.0), y * sqrt(1.0 - x * x / 2.0)


# if the coordinate is an index in an image it's between 0 and the length of the image
# we need it to be between -1 and 1 for the math
def pixel_coordinates_to_one(coordinate, max_value):
    return coordinate / max_value * 2 - 1


def one_coordinates_to_pixels(coordinate, max_value):
    return (coordinate + 1) / 2 * max_value


def check_that_all_sides_are_the_same_length(inp):
    for x, row in enumerate(inp):
        if len(row) != len(inp):
            raise ValueError(
                f"The input image must be square shaped but row {x} "
                f"is {len(row)} pixels accross, while the other side of the "
                f"image is {len(inp)}"
            )


def transform(inp, coordinate_transformer=fgs_square_to_disc):
    # TODO: you should be able to extend this to rectangles and ovals
    check_that_all_sides_are_the_same_length(inp)

    result = np.zeros_like(inp)

    for x, row in enumerate(inp):
        # convert pixel coordinates to TODO: what is this called? it's not a unit square
        # x and y are in the range(0, len(inp)) but they need to be between -1 and 1
        # for the code
        unit_x = pixel_coordinates_to_one(x, len(inp))

        for y, _ in enumerate(row):
            unit_y = pixel_coordinates_to_one(y, len(row))

            try:
                uv = coordinate_transformer(unit_x, unit_y)
                if uv is None:
                    continue
                u, v = uv

                u = one_coordinates_to_pixels(u, len(inp))
                v = one_coordinates_to_pixels(v, len(row))

                # TODO: something smarter.
                # maybe take the average of the nearest 4 pixels
                result[x][y] = inp[floor(u)][floor(v)]
            except IndexError:
                pass

    return result


methods = {
    "fgs": {"to_square": fgs_disc_to_square, "to_disc": fgs_square_to_disc},
    "simple_stretch": {
        "to_square": simple_stretch_disc_to_square,
        "to_disc": simple_stretch_square_to_disc,
    },
    "elliptical": {
        "to_square": elliptical_disc_to_square,
        "to_disc": elliptical_square_to_disc,
    },
    # TODO: Schwarz-Christoffel
    # https://squircular.blogspot.com/2015/09/schwarz-christoffel-mapping.html
}


def check_method_is_valid(method):
    if method not in methods:
        raise ValueError(
            f'"{method}" is not a valid method. '
            f'The choices are {" and ".join(", ".join(methods.keys()).rsplit(", ", 1))}.'
        )


def to_square(disk, method="fgs"):
    check_method_is_valid(method)
    # using square_to_disc to convert discs to squares is counterintuitive
    return transform(disk, methods[method]["to_disc"])


def to_disk(square, method="fgs"):
    check_method_is_valid(method)
    # using disc_to_square to convert squares to discs is counterintuitive
    return transform(square, methods[method]["to_square"])
