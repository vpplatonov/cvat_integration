import cv2
import numpy as np

from ellipse_to_poligon import (
    get_points_from_ellipse
)

ELLIPSE_PARAM = dict(
    _xc=626.772705,
    _yc=381,
    _a=198,
    _b=39.5999985,
    _rad=3.141593,
    _score=0.67299813,
)


def test_ellipse_detector():
    assert isinstance(ELLIPSE_PARAM, dict)


def test_get_points_from_ellipse():

    poligon = get_points_from_ellipse(((0, 0), (7, 4), 36))

    assert len(poligon) == 66

    xc, yc, a, b, rad, _ = ELLIPSE_PARAM.values()

    poligon = get_points_from_ellipse(ellipse=((xc, yc), (a, b), rad * 180.0 / 3.1415926))

    assert len(poligon) == 65
    assert poligon.shape == (65, 2)


def test_geom():
    contours = np.array([[50, 50], [50, 150], [150, 150], [150, 50]])
    img = np.zeros((200, 200))  # create a single channel 200x200 pixel black image
    cv2.fillPoly(img, pts=[contours], color=(255, 255, 255))
    cv2.imshow(" ", img)
    cv2.waitKey()
