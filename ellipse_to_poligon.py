import cv2
import numpy as np

import shapely.affinity
from shapely.geometry import Point

ELLIPSE_PARAM = dict(
    _xc=626,
    _yc=381,
    _a=198,
    _b=40,
    _rad=3.141593,
    _score=0.67299813,
)


def get_points_from_ellipse(ellipse):
    # 1st elem = center point (x,y) coordinates
    # 2nd elem = the two semi-axis values (along x, along y) a, b
    # 3rd elem = angle in degrees between x-axis of the Cartesian base
    #            and the corresponding semi-axis

    # Let create a circle of radius 1 around center point:
    circ = shapely.geometry.Point(ellipse[0]).buffer(1)

    # Let create the ellipse along x and y:
    ell = shapely.affinity.scale(circ, int(ellipse[1][0]), int(ellipse[1][1]))

    # Let rotate the ellipse (clockwise, x axis pointing right):
    ellr = shapely.affinity.rotate(ell, ellipse[2])

    return np.array([[int(coord[0]), int(coord[1])] for coord in list(ellr.exterior.coords)])


if __name__ == '__main__':
    image = cv2.imread('../ellipse-detector/image/soccer_frame_1.jpg')

    cv2.imshow('Ellipse_to_Poligon', image)
    cv2.waitKey(0)

    xc, yc, a, b, rad, _ = ELLIPSE_PARAM.values()
    # poligon = get_points_from_ellipse(ellipse=((xc, yc), (a, b), rad * 180.0 / 3.1415926))

    num_points = 15
    poligon = cv2.ellipse2Poly((xc, yc), (a, b), int(rad * 180.0 / 3.1415926), 0, 360, int(360 / num_points))

    # img = cv2.fillPoly(image, pts=[poligon], color=(0, 0, 255))
    img = cv2.drawContours(image, contours=[poligon], contourIdx=-1, color=(0, 0, 255), thickness=2)

    cv2.imshow('Ellipse_to_Poligon', img)
    cv2.waitKey(0)

    # close all windows
    cv2.destroyAllWindows()
