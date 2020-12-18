import numpy as np
import os
import sys
import cv2

sys.path.append(os.path.abspath('serverless/opencv/ellipse_detection/nuclio'))
from model_loader import (
    ModelLoader, POLYGON_SHAPE_TYPE
)

Ellipse_LABELS = [
    {"id": 0, "name": "Ellipse"}
]


class EllipseDetector:
    def __init__(self, threshold=0.65, radius_threshold_divider=40):
        """
        :param threshold: score
        :param radius_threshold_divider: limit the min ellipses radius: 0 - all
        """
        self.model_handler = ModelLoader(Ellipse_LABELS)
        self.threshold = threshold
        self.r_thrd = radius_threshold_divider

    def detect(self, frame, width=1280, shape_type=POLYGON_SHAPE_TYPE):
        # run detector
        results = self.model_handler.infer(
            np.array(frame),
            threshold=self.threshold,
            r_thrd=width / self.r_thrd if self.r_thrd > 1 else width,
            shape_type=shape_type
        )

        # clustering by distance & sort by score & return with max score in each cluster
        if len(results):
            results = self.clustering_max_score(results, threshold=300)

        return results

    @staticmethod
    def clustering_max_score(ellipses, threshold=100):
        # clustering
        gr = 0
        groups = {f'{gr}': [ellipses[0]["ellipse"]]}
        for ellipse in ellipses[1:]:
            added = False
            for gid, group in groups.items():
                if np.linalg.norm(np.array(list(ellipse["ellipse"].values())[:2]) -
                                  np.array(list(group[0].values())[:2])) < threshold:
                    groups[gid].append(ellipse["ellipse"])
                    added = True
            if not added:
                gr += 1
                groups[f'{gr}'] = [ellipse["ellipse"]]

        # find max score in each cluster
        results = {gid: groups[gid][0] for gid in set(groups.keys())}
        for gid, group in groups.items():
            for ellipse in group[1:]:
                if ellipse["_score"] > results[gid]["_score"]:
                    results[gid] = ellipse

        results = [ellipse for ellipse in list(results.values())]

        return results

    @staticmethod
    def get_points_from_ellipse_param(ellipse, num_points=8):
        xc, yc, a, b, rad, score = ellipse["ellipse"].values()
        angle = int(rad * 180.0 / np.pi)
        # start_angle = int(angle / 2)
        contour = cv2.ellipse2Poly(
            (xc, yc),
            (a, b),
            angle,
            0,  # start_angle,  # if angle > 0 else 180 - angle,
            360,  # + start_angle,  # if angle > 0 else ,
            int(360 / num_points)
        )

        return contour

    @staticmethod
    def get_points_from_ellipse(ellipse):
        points = ellipse["points"] if "points" in ellipse else ellipse
        points = [[points[i], points[i + 1]] for i in range(0, len(points), 2)]

        return points

    @staticmethod
    def m_ap_precision(ellipse=None, gt_ellipse=None):
        """
        Calculates how accurate detection is
        :param ellipse: Object detected by detector
        :param gt_ellipse: GroundTrue points from CVAT annotation
        :return:
        """
        if ellipse is None:
            return 0
