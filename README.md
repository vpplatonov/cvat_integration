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

{'_xc': '236.69', '_yc': '155.871', '_a': '24', '_b': '17.52', '_rad': '2.94961', '_score': '0.971709'}
{'_xc': '311.22', '_yc': '246.163', '_a': '27', '_b': '20.25', '_rad': '3.00197', '_score': '0.931649'}
{'_xc': '250.711', '_yc': '276.921', '_a': '28', '_b': '20.72', '_rad': '2.77507', '_score': '0.908392'}
{'_xc': '123.281', '_yc': '208.007', '_a': '26', '_b': '18.46', '_rad': '2.6529', '_score': '0.908055'}
{'_xc': '212.087', '_yc': '225.196', '_a': '26', '_b': '20.54', '_rad': '2.70526', '_score': '0.858707'}
{'_xc': '97.3799', '_yc': '165.463', '_a': '24', '_b': '16.56', '_rad': '2.58309', '_score': '0.853357'}
```
