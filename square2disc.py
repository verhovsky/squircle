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


def pixel_coordinates_to_one(coordinate, max_value):
    return coordinate / max_value * 2 - 1


def one_coordinates_to_pixels(coordinate, max_value):
    return (coordinate + 1) / 2 * max_value


def transform(inp, coordinate_transformer=fgs_square_to_disc):
    result = np.zeros_like(inp)

    for x, row in enumerate(inp):
        # TODO: you should be able to extend this stuff to rectangles and ovals
        if len(row) != len(inp):
            raise ValueError(
                f"The input image must be square shaped, but it's {len(row)} by {len(inp)}"
            )

        # convert pixel coordinates to TODO: what is this called?
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


def to_square(circle, method="fgs"):
    # TODO: using square_to_disc to convert discs to squares is unintuitive
    return transform(circle, fgs_square_to_disc)


def to_circle(square, method="fgs"):
    # TODO: using disc_to_square to convert squares to discs is unintuitive
    return transform(square, fgs_disc_to_square)
