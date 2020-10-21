# cvat_integration

## run ellipse_detector
-N image Name
-D DataSet Name
-S The threshold of ellipse score
-R The threshold of Reliability
-C The threshold of CenterDis
-M The method id
-P Working Directory
```
serverless/opencv/ellipse_detection/bin/ellipse_detector  -N 027_0003.jpg  -S 0.85 -P . -M 9
```
image files shoud be inside images dir

## python module
Python running executable as subprocess
```
python tests/test_subprocess_popen.py
```
