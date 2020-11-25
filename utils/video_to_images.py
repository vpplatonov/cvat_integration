import cv2 as cv


def set_stream_frame(cap, frame_num):
    """
    if cap.set() do not work
    :param cap:
    :param frame_num:
    :return:
    """
    if frame_num == 0:
        return

    cap.set(cv.CAP_PROP_POS_FRAMES, frame_num)
    current_frame = cap.get(cv.CAP_PROP_POS_FRAMES)
    if current_frame < frame_num:
        while True:
            # change read() to grab() / retrieve()
            success, frame = cap.grab()
            if not success:
                raise Exception('cant read frames')
            if cap.get(cv.CAP_PROP_POS_FRAMES) == frame_num:
                break


if __name__ == "__main__":

    video_path = '../../VideoImages/soccer_ex06.avi'
    cap = cv.VideoCapture(video_path)
    if not cap.isOpened():
        print(f'file {video_path} not available')

    frames_count = cap.get(cv.CAP_PROP_FRAME_COUNT)
    w = cap.get(cv.CAP_PROP_FRAME_WIDTH)
    h = cap.get(cv.CAP_PROP_FRAME_HEIGHT)

    # start stop frames should be paired like [1, 5, 300, 325]
    start_stop_frames = [400, 405, 600, 605]
    assert len(start_stop_frames) % 2 == 0
    assert start_stop_frames[-1] < frames_count

    for rng in range(0, len(start_stop_frames) // 2):
        start = rng * 2
        try:
            set_stream_frame(cap, start_stop_frames[start])
        except Exception as e:
            print(e)
            continue

        # repetitive read
        for i in range(start_stop_frames[start], start_stop_frames[start + 1]):
            success, frame = cap.read()
            if not success:
                break

            current_frame = int(cap.get(cv.CAP_PROP_POS_FRAMES))
            image_name = f"{video_path.split('.avi')[0]}_{current_frame}.jpg"
            # save to project path
            image_name = 'output/' + image_name.split('/')[-1]
            cv.imwrite(image_name, frame)

    cap.release()
