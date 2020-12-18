# Copyright (C) 2020 Global Logic
#
# SPDX-License-Identifier: MIT

import cv2
import os
import subprocess
import numpy as np

ELLIPSE_PARAM = dict(
    _xc=626,
    _yc=381,
    _a=198,
    _b=40,
    _rad=3.141593,
    _score=0.67299813,
)

POLYGON_SHAPE_TYPE = "polygon"


def execute(cmd):
    """RUN one-sub in subprocess with line by line output

    :param cmd: array of command and params
    :return:
    """
    print(f"Execute command: {' '.join(cmd)}")
    popen = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        universal_newlines=False,
        # bufsize=1,  # unbuffered
    )
    for stdout_line in iter(popen.stdout.readline, b''):
        yield stdout_line

    popen.stdout.close()
    popen.kill()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def ellipse_detection_in_subprocess(image):
    ellipses = []
    ell_keys = list(ELLIPSE_PARAM.keys())
    if image.shape[0]:
        # command = [
        #     'ellipse_detector',
        #     '-N', 'image_frame.jpg',
        #     '-S', '0.85',
        #     '-P', '.',
        #     '-M', '9'
        # ]
        command = [
            'AAMED',
            'image_frame.jpg'
        ]

        os.makedirs('images', exist_ok=True)
        cv2.imwrite('images/image_frame.jpg', image)

    else:
        command = [
            'AAMED',
            '027_0003.jpg'
        ]

    for line in execute(command):
        ell = line.split(b"\t")
        if ell[0].decode('utf-8') == 'ellipse':
            ellipse = {ell_keys[key]: (int(float(el.decode('utf-8').strip()))
                                       if key < 4 else float(el.decode('utf-8').strip()))
                       for key, el in enumerate(ell[1:])}
            ellipses.append(ellipse)

    if image.shape[0]:
        os.remove('images/image_frame.jpg')

    return ellipses


class ModelLoader:
    def __init__(self, labels):
        self.labels = labels
        self.num_points = 15

        class EllipseDetector:
            def detect(self, images):
                # import ed.so module to work with
                ellipses_param = []
                for image in images:
                    ellipses = ellipse_detection_in_subprocess(image)
                    ellipses_param.append(ellipses)
                return ellipses_param
                # return [[ELLIPSE_PARAM]]

        self.model = EllipseDetector()

    def infer(self, image, threshold=0.85, r_thrd=0, shape_type=POLYGON_SHAPE_TYPE, logger=None):

        output = self.model.detect([image])[0]
        if image.shape[0]:
            (h, w) = image.shape[:2]
            if r_thrd == 0:
                r_thrd = w / 70  # all ellipse with r < 30 are noise

        results = []
        for i in range(len(output)):
            class_id = 0
            label = self.labels[class_id]
            xc, yc, a, b, rad, score = output[i].values()
            if logger is not None:
                logger.info(f"xc {xc}, yc {yc}, a {a}, b {b}, rad {rad}, score {score}")

            if score >= threshold and b > r_thrd:
                if shape_type == POLYGON_SHAPE_TYPE:
                    contour = cv2.ellipse2Poly(
                        (xc, yc),
                        (a, b),
                        int(rad * 180.0 / np.pi),
                        0,
                        360,
                        int(360 / self.num_points)
                    )

                    # filter all points left from center
                    poli_left = np.array([np.concatenate((point, np.array([int(i)])))
                                          for i, point in enumerate(contour) if point[0] < xc])
                    idx = int(poli_left[np.absolute(poli_left[:, 1] - yc).argmin()][2])
                    # reorganize poligon
                    poligon_first = [point for point in contour[idx:-1]]
                    contour = np.array(poligon_first + [point for point in contour[:idx]] + [poligon_first[0]])

                    results.append({
                        "confidence": str(score),
                        "label": label,
                        "points": contour.ravel().tolist(),
                        "type": shape_type,
                    })
                else:
                    results.append({
                        "confidence": str(score),
                        "label": label,
                        "ellipse": output[i],
                        "type": shape_type,
                    })

        return results
