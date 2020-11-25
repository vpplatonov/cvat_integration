import numpy as np
import os
import sys

sys.path.append(os.path.abspath('serverless/opencv/ellipse_detection/nuclio'))
from model_loader import (
    ModelLoader
)

Ellipse_LABELS = [
    {"id": 0, "name": "Ellipse"}
]


class EllipseDetector:
    def __init__(self):
        self.model_handler = ModelLoader(Ellipse_LABELS)

    def detect(self, frame, width=1280):
        # run detector
        results = self.model_handler.infer(
            np.array(frame),
            threshold=0.85,
            r_thrd=width / 40,
        )

        return results

    @staticmethod
    def get_points_from_ellipse(ellipse):
        points = ellipse["points"]
        points = [[points[i], points[i + 1]] for i in range(0, len(points), 2)]

        return points
