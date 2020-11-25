import cv2 as cv

from dumps.sequence_manager import SequenceManager

if __name__ == "__main__":
    gt_annotations_file = 'dumps/gt_cvat_for_video_1.1/annotations.json'
    video_file = '../AnnotationBenchmarks/14701073_25831_5200_11200.mkv'

    sm = SequenceManager(video_path=video_file, ground_truth_path=gt_annotations_file)

    while True:
        sm.find_next_gt_frame()
        gt = sm.get_gt()
        frame = sm.get_frame()
        if frame is None:
            break
        # draw gt on image
        for obj in gt.keys():
            if obj == 'frame':
                continue
            points = list(gt[obj].values())[0]
            for idx in range(0, len(points) - 1):
                cv.line(
                    frame,
                    (points[idx][0], points[idx][1]),
                    (points[idx + 1][0], points[idx + 1][1]),
                    color=(0, 255, 0),
                    thickness=2
                )

        cv.imshow('frames', frame)
        cv.waitKey(1)
