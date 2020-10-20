# Copyright (C) 2020 Global Logic
#
# SPDX-License-Identifier: MIT

import cv2

ELLIPSE_PARAM = dict(
    _xc=626,
    _yc=381,
    _a=198,
    _b=40,
    _rad=3.141593,
    _score=0.67299813,
)

PI = 3.1415926


class ModelLoader:
    def __init__(self, labels):
        self.labels = labels
        self.num_points = 15

        class EllipseDetector:
            def detect(self, images):
                # import ed.so module to work with
                return [[ELLIPSE_PARAM]]

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
