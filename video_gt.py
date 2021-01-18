import cv2 as cv
import os
from dumps.sequence_manager import SequenceManager
from ellipse_detector import EllipseDetector
import numpy as np
import json


def cv_draw_points(points, frame, color=(0, 255, 0), thickness=2):
    for idx in range(0, len(points) - 1):
        cv.line(
            frame,
            (points[idx][0], points[idx][1]),
            (points[idx + 1][0], points[idx + 1][1]),
            color=color,
            thickness=thickness
        )


def gt_draw_object(gt_obj, frame, color=(0, 255, 0), thickness=2):
    """
    Draw tracked object @id on image
    :param gt_obj: single track from annotation
    :param frame: RGB
    :param color: (0, 255, 0)
    :param thickness of line
    :return:
    """
    points = list(gt_obj.values())[0]
    cv_draw_points(points, frame, color=(0, 255, 0), thickness=2)


if __name__ == "__main__":
    # gt_annotations_file = 'dumps/gt_cvat_for_video_1.1/14701073_25831_5200_11200_mkv_annotations.json'
    # video_file = '../AnnotationBenchmarks/14701073_25831_5200_11200.mkv'
    gt_annotations_file = None
    video_file = '../VideoImages/14701073_25831_11200_61200.mp4'
    output = None  # 'output'
    ellipse_detections = []
    file_name = video_file.split('/').pop().split('.')[0]

    sm = SequenceManager(
        video_path=video_file,
        ground_truth_path=gt_annotations_file,
        output=output
    )
    ellipse_detector = EllipseDetector()

    try:
        while True:
            if gt_annotations_file is not None:
                # for GT anotation
                sm.find_next_gt_frame()
                gt = sm.get_gt()
                if len(gt.keys()) == 1:
                    # annotations ended
                    break
                frame = sm.get_frame()
                if frame is None:
                    break

                # draw gt on image
                for key in gt.keys():
                    # if key != 'Ellipse':
                    if key == 'frame':
                        continue
                    gt_draw_object(gt[key], frame)

                # run detector & draw detections
                results = ellipse_detector.detect(frame, width=sm.w)
                for ellipse in results:
                    points = ellipse_detector.get_points_from_ellipse(ellipse)
                    cv_draw_points(points, frame, color=(0, 0, 255), thickness=2)

            else:
                # for detection
                frame = sm.get_next_frame()
                results = ellipse_detector.detect(frame, width=sm.w, shape_type="ellipse")
                if len(results) > 1:
                    print(f"{results}")
                for ellipse in results:
                    xc, yc, a, b, rad, score = ellipse.values()
                    cv.ellipse(
                        frame,
                        (xc, yc),
                        (int(a), int(b)),
                        int(rad * 180 / np.pi),
                        0, 360,
                        color=(255, 0, 0),
                        thickness=3
                    )

            cv.imshow('frames', frame)
            key = cv.waitKey(1) & 0xFF
            if key == ord("s"):
                break

            if sm.writer is not None:
                sm.writer.write(frame)

            ellipse_detections.append({
                "frame": sm.current_frame,
                "Ellipse": [[val for val in ellipse.values()] for ellipse in results]
            })

    except Exception as e:
        print(e)
    finally:
        if sm.writer is not None:
            sm.writer.release()

        with open(os.path.join('output_video', f"{file_name}_ellipses.json"), "w") as fp:
            json.dump(ellipse_detections, fp)
        cv.destroyAllWindows()
        sm.cap.release()
