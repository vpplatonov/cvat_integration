import cv2 as cv
import json
import os

from .merge_tracks import get_label

# for 14701073_25831_11200_61200.mp4: X - excluded from GT
dct_keyframes = {
    0: 'C', 326: 'R', 656: 'X', 763: 'R', 1034: 'X', 1131: 'R', 1167: 'C', 1284: 'X', 1506: 'C', 1896: 'X',
    # 0: 'X', 326: 'X', 656: 'X', 763: 'X', 1034: 'X', 1131: 'X', 1167: 'X', 1284: 'X', 1506: 'X', 1896: 'X',
    # 1951: 'X', 2262: 'X', 2327: 'X', 2749: 'X', 3199: 'L', 3613: 'C', 4049: 'R',
    1951: 'C', 2262: 'R', 2327: 'C', 2749: 'X', 3199: 'L', 3613: 'C', 4049: 'R',
    4163: 'C', 4371: 'X', 5134: 'C', 5415: 'L', 6114: 'X', 6349: 'C', 6558: 'R', 6746: 'C', 7209: 'X',
    7274: 'C', 7483: 'X', 7624: 'C', 8077: 'R', 8823: 'X', 8916: 'C', 9082: 'R',
    9276: 'C', 9360: 'R', 9459: 'C', 9813: 'X', 9966: 'C', 10204: 'L', 10389: 'X', 10774: 'R', 11175: 'C',
    11551: 'R', 11847: 'C', 12010: 'R', 12053: 'X', 12299: 'R', 12476: 'X', 12558: 'R',
    12958: 'C', 14048: 'R', 14374: 'C', 15348: 'X', 15409: 'C', 15478: 'X', 15608: 'C', 16098: 'R',
    16181: 'X', 18196: 'R', 19201: 'X', 20616: 'R', 20981: 'X', 21118: 'R', 21378: 'X', 21416: 'R',
    21591: 'X', 21836: 'R', 22241: 'C', 22761: 'X', 22808: 'C', 22909: 'X', 23084: 'C', 23928: 'X',
    23969: 'C', 24060: 'L', 24818: 'X', 25342: 'L', 25968: 'C', 26446: 'X', 27269: 'C', 27483: 'R',
    28439: 'C', 29926: 'X', 30071: 'C', 30334: 'X', 30438: 'R', 30525: 'C', 30684: 'X', 30749: 'C',
    31468: 'X', 31686: 'C', 32167: 'L', 32624: 'X', 32903: 'L', 33264: 'X', 34096: 'L', 34647: 'C',
    35281: 'X', 35354: 'C', 36686: 'R', 36984: 'X', 37091: 'R', 37194: 'C', 37628: 'X', 37706: 'C',
    38279: 'L', 38501: 'X', 38878: 'L', 38922: 'C', 39279: 'R', 39641: 'X', 39909: 'C', 40374: 'L',
    40519: 'C', 40721: 'X', 40768: 'C', 40850: 'R', 41414: 'C', 41950: 'L', 41994: 'X', 42239: 'R',
    42967: 'C', 43130: 'R', 43300: 'C', 43353: 'X', 43506: 'C', 43586: 'L', 43699: 'X', 44828: 'E'
}


class SequenceManager:
    def __init__(self, video_path=None, ground_truth_path=None, output=None):

        if ground_truth_path is not None:
            with open(ground_truth_path, 'r') as fp:
                self.doc = json.load(fp)

            # check doc meta source the same as file name in video_path
            assert self.doc['annotations']["meta"]["source"] == video_path.split("/")[-1], \
                "annotation source & video path are different"
        else:
            self.doc = None

        self.cap = cv.VideoCapture(video_path)
        self.frames_count = int(self.cap.get(cv.CAP_PROP_FRAME_COUNT))
        self.w = self.cap.get(cv.CAP_PROP_FRAME_WIDTH)
        self.h = self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)
        self.fps = self.cap.get(cv.CAP_PROP_FPS)

        # find first frame @id for start
        self.current_frame = 0
        self.frame_excluded = self.get_excluded_frames_range()
        self.writer = None

        if output:
            fourcc = cv.VideoWriter_fourcc(*'mp4v')
            file_name = video_path.split('/').pop().split('.')[0]
            out_file = os.path.join(output, f"{file_name}.mp4")
            assert isinstance(fourcc, int), f"fourcc must be int {fourcc}"
            self.writer = cv.VideoWriter(
                out_file,
                fourcc,
                self.fps,
                (self.w, self.h),
                True
            )

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

        self.current_frame = int(self.cap.get(cv.CAP_PROP_POS_FRAMES))
        success, frame = self.cap.read()
        if not success:
            return None

        return frame

    def get_next_frame(self):

        self.set_next_image()

        self.current_frame = int(self.cap.get(cv.CAP_PROP_POS_FRAMES))
        success, frame = self.cap.read()
        if not success:
            return None

        return frame

    def set_next_image(self):
        curr_fr_num = int(self.cap.get(cv.CAP_PROP_POS_FRAMES))
        next_fr_num = None
        for fr_range in self.frame_excluded:
            if fr_range[0] <= curr_fr_num + 1 <= fr_range[1]:
                next_fr_num = fr_range[1] + 1
                break

        if next_fr_num is not None:
            if next_fr_num <= self.frames_count:
                self.cap.set(cv.CAP_PROP_POS_FRAMES, next_fr_num)
                self.current_frame = next_fr_num
            else:
                raise Exception("All frames processed")

    @staticmethod
    def get_included_frames_range():
        include_ranges = []
        start_frame = None

        for key in dct_keyframes.keys():
            if dct_keyframes[key] == 'X':
                if start_frame is not None:
                    include_ranges.append([start_frame, key])
                    start_frame = None
            else:
                if start_frame is None:
                    start_frame = key

        return include_ranges

    @staticmethod
    def get_excluded_frames_range():
        exclude_range = []
        start_frame = None

        for key in dct_keyframes.keys():
            if dct_keyframes[key] == 'X':
                if start_frame is None:
                    start_frame = key
            else:
                if start_frame is not None:
                    exclude_range.append([start_frame, key])
                    start_frame = None

        return exclude_range
