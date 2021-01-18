import glob

import cv2
import os
from pathlib import Path

if __name__ == "__main__":
    # List all files in directory using pathlib
    basepath = Path('../output/')
    files_in_basepath = glob.glob(f"{basepath}/*.jpg")
    files_in_basepath = sorted(
        files_in_basepath,
        key=lambda x: int(x.split("_").pop().split(".")[0])
    )
    # get size of frame
    image = cv2.imread(str(files_in_basepath[0]))
    size_hw = image.shape[:2]

    # create video writer
    fps = 10
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    file_name = files_in_basepath[0].split('/').pop().split(".")[0]
    writer = cv2.VideoWriter(
        os.path.join("./", f"{file_name}.mp4"),
        fourcc,
        fps,
        (size_hw[1], size_hw[0]),
        True
    )

    for file in files_in_basepath:
        print(str(file))
        filename_in = cv2.imread(str(file))
        cv2.imshow("img", filename_in)
        cv2.waitKey(1)
        writer.write(filename_in)

    writer.release()
    cv2.destroyAllWindows()
