import cv2 as cv

from dumps.sequence_manager import SequenceManager
from ellipse_detector import EllipseDetector


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
    gt_annotations_file = 'dumps/gt_cvat_for_video_1.1/14701073_25831_5200_11200_mkv_annotations.json'
    video_file = '../AnnotationBenchmarks/14701073_25831_5200_11200.mkv'

    sm = SequenceManager(video_path=video_file, ground_truth_path=gt_annotations_file)
    ellipse_detector = EllipseDetector()

    while True:
        sm.find_next_gt_frame()
        gt = sm.get_gt()
        if len(gt.keys()) == 1:
            # annotations ended
            break
        frame = sm.get_frame()
        if frame is None:
            break

        # run detector & draw detections
        results = ellipse_detector.detect(frame, width=sm.w)
        for ellipse in results:
            points = ellipse_detector.get_points_from_ellipse(ellipse)
            cv_draw_points(points, frame, color=(0, 0, 255), thickness=2)

        # draw gt on image
        for key in gt.keys():
            # if key != 'Ellipse':
            if key == 'frame':
                continue
            gt_draw_object(gt[key], frame)

        cv.imshow('frames', frame)
        cv.waitKey(1)

    cv.destroyAllWindows()
    sm.cap.release()
