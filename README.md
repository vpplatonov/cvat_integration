# cvat_integration

## run ellipse_detector
[https://github.com/vpplatonov/ellipse_detector]
-N image Name
-D DataSet Name
-S The threshold of ellipse score
-R The threshold of Reliability
-C The threshold of CenterDis
-M The method id
-P Working Directory
```
$ serverless/opencv/ellipse_detection/bin/ellipse_detector  -N 027_0003.jpg  -S 0.85 -P . -M 9

ellipse 236.69  155.871 24      17.52   2.94961 0.971709
ellipse 311.22  246.163 27      20.25   3.00197 0.931649
ellipse 250.711 276.921 28      20.72   2.77507 0.908392
ellipse 123.281 208.007 26      18.46   2.6529  0.908055
ellipse 212.087 225.196 26      20.54   2.70526 0.858707
ellipse 97.3799 165.463 24      16.56   2.58309 0.853357

```

image files should be inside images dir

## python module
Python running executable as subprocess
```
$ python tests/test_subprocess_popen.py
Execute command: serverless/opencv/ellipse_detection/bin/ellipse_detector -N 027_0003.jpg -S 0.85 -P . -M 9
{'_xc': 236, '_yc': 155, '_a': 24, '_b': 17, '_rad': 2.94961, '_score': 0.971709}
{'_xc': 311, '_yc': 246, '_a': 27, '_b': 20, '_rad': 3.00197, '_score': 0.931649}
{'_xc': 250, '_yc': 276, '_a': 28, '_b': 20, '_rad': 2.77507, '_score': 0.908392}
{'_xc': 123, '_yc': 208, '_a': 26, '_b': 18, '_rad': 2.6529, '_score': 0.908055}
{'_xc': 212, '_yc': 225, '_a': 26, '_b': 20, '_rad': 2.70526, '_score': 0.858707}
{'_xc': 97, '_yc': 165, '_a': 24, '_b': 16, '_rad': 2.58309, '_score': 0.853357}
```

## test
before test copy serverless/opencv/ellipse_detection/bin/ellipse_detector into ~/bin dir OR /usr/local/bin
```
$ pytest tests/test_subprocess_popen.py 
```

## Deploy
### Docker build
[https://hub.docker.com/r/jjanzic/docker-python3-opencv/dockerfile]
```
$ docker build -f docker/dockerfile --tag jjanzic/docker-python3-opencv:contrib-opencv-3.4.11 .
```
### nucleo deploy
```
$ cd serverless/
$ ./deploy.sh
```
### Test inside docker
```
$ docker exec -it nuclio-nuclio-opencv.ellipse_detector ellipse_detector -N 027_0003.jpg  -S 0.85 -P . -M 9
```

### Up CVAT
[https://github.com/openvinotoolkit/cvat/tree/develop/components/serverless]
