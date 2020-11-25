import cv2 as cv
import json

from .merge_tracks import get_label


class SequenceManager:
    def __init__(self, video_path=None, ground_truth_path=None):

        with open(ground_truth_path, 'r') as fp:
            self.doc = json.load(fp)

        # check doc meta source the same as file name in video_path
        assert self.doc['annotations']["meta"]["source"] == video_path.split("/")[-1], \
            "annotation source & video path are different"

        self.cap = cv.VideoCapture(video_path)
        self.frames_count = int(self.cap.get(cv.CAP_PROP_FRAME_COUNT))
        w = self.cap.get(cv.CAP_PROP_FRAME_WIDTH)
        h = self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)

        # find first frame @id for start
        self.current_frame = 0

    def find_next_gt_frame(self):
        next_frame = self.frames_count
        for track in self.doc["annotations"]["track"]:
            label, label_shape_type = get_label(track)
            for obj in track[label_shape_type]:
                if obj["@outside"] == '1':
                    continue
                if self.current_frame < int(obj["@frame"]) < next_frame:
                    next_frame = int(obj["@frame"])

        self.current_frame = next_frame

    def get_gt(self, frame_num=None):

        if frame_num is None:
            frame_num = self.current_frame
        gt = dict(
            frame=frame_num
        )
        for track in self.doc["annotations"]["track"]:
            label, label_shape_type = get_label(track)
            points_gen = filter(lambda x: x["@frame"] == str(frame_num), track[label_shape_type])
            try:
                points = next(points_gen)
            except Exception as e:
                pass
            else:
                points = points["@points"]
                attribute = ''
                if "attribute" in track[label_shape_type][0]:
                    attribute = f'_{track[label_shape_type][0]["attribute"]["#text"]}'
                gt[f"{label}{attribute}"] = {
                    label_shape_type: [[int(float(coord)) for coord in point.split(',')] for point in points.split(';')]
                }

        return gt

    def get_frame(self, frame_num=None):
        # video
        if frame_num is None:
            frame_num = self.current_frame
            self.cap.set(cv.CAP_PROP_POS_FRAMES, frame_num)

        success, frame = self.cap.read()
        if not success:
            return None

        # self.current_frame = self.cap.get(cv.CAP_PROP_POS_FRAMES)

        return frame
