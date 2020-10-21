# Copyright (C) 2020 Global Logic
#
# SPDX-License-Identifier: MIT

import cv2
import os
import subprocess

ELLIPSE_PARAM = dict(
    _xc=626,
    _yc=381,
    _a=198,
    _b=40,
    _rad=3.141593,
    _score=0.67299813,
)

PI = 3.1415926


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
        bufsize=1,  # unbuffered
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
    command = [
        'ellipse_detector',
        '-N', 'image_frame.jpg',
        '-S', '0.85',
        '-P', '.',
        '-M', '9'
    ]
    ell_keys = list(ELLIPSE_PARAM.keys())

    os.makedirs('images',exist_ok=True)
    cv2.imwrite('images/image_frame.jpg', image)

    for line in execute(command):
        ell = line.split(b"\t")
        if ell[0].decode('utf-8') == 'ellipse':
            ellipses.append(
                {ell_keys[key]: el.decode('utf-8').strip()
                 for key, el in enumerate(ell[1:])}
           )

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

    def infer(self, image, threshold=0.85):
        output = self.model.detect([image])[0]

        results = []
        for i in range(len(output)):
            class_id = 0
            xc, yc, a, b, rad, score = output[i].values()

            if score >= threshold:
                contour = cv2.ellipse2Poly(
                    (xc, yc),
                    (a, b),
                    int(rad * 180.0 / PI),
                    0,
                    360,
                    int(360 / self.num_points)
                )
                label = self.labels[class_id]

                results.append({
                    "confidence": str(score),
                    "label": label,
                    "points": contour.ravel().tolist(),
                    "type": "polygon",
                })

        return results
