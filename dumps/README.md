## soccer field annotation 
Task should be done in CVAT Annotation tools inside VPN network

CVAT user guide
https://github.com/openvinotoolkit/cvat/blob/develop/cvat/apps/documentation/user_guide.md

### Short overview

#### Create task

It's possible use for train purpose already uploaded task (#7 by ex.)
or ask for task preparation.

#### Types of object should be annotated

1. Ellipse

2. Boundary line with additional attributes:

    upper
    lower
    left
    right
    middle

3. Line ( penalty area of soccer field left & right) with additional attributes:

    left_upper_big_horizon
    left_upper_small_horizon
    left_lower_small_horiz
    left_lower_big_horiz
    left_big_sloped
    left_small_sloped
    right_upper_big_horizon
    right_upper_small_horizon
    right_lower_small_horiz
    right_lower_big_horiz
    right_big_sloped
    right_small_sloped

#### Default Setting should be changed

1. <user>-> Settings -> Player -> Player step
change from 10 to 30 or 40 or more for comfortable annotating

2. Inside annotation job in left bar Objects -> Sort by
change to "updated time" 
in this case last editable object will be always on top of objects list ( it minimize time to find Obj you are working with)

##### Steps for keyframe
Shape objects on the first selected key frame ( by ex 1) 

1. Ellipse

select "magic wand" on left sidebar ( "AI Tools" window will popup )
select "Detectors" -> Model "Ellipse Detector" -> Ellipse to Ellipse map -> press Annotate

Ellipse in the middle of field should be annotates as poligon with 15 points

Issue: No ellipse was marked
Solution: select next frame as keyframe for detection

Issues: marked 2 or more ellipses
Solution: Move mouse above wrong object and use Del key press to remove it; Must be left only one - big central soccer field ellipse

2. Boundary lines

- select "Draw new polyline" -> Label "boundary line" -> Number of points "2" -> press "Shape" button
- cursor will change to "+" sign
- press mouse button on start line point and then press second on end of line point
- look on right side bar : this object should be on top of list; select valid attribute in Details drop down list ( see above )

Issue: There are not all boundary lines visible
Solution: should be marked only visible lines

3. Lines

procedure same as for Boundary lines

#### Tracking and interpolation between keyframes

You do not need to annotate each frame
Most of them can be marked automatically by CVAT
Steps should be
    - choose next key frame ( by ex 31). simple press >> button on player bar
Mark
    - annotate 30 frame as described in "Steps for keyframe"
Track
    - merge objects between 30 and 1 keyframes
    - use "merge shapes/tracks" on left sidebar: 
        cursor will change to "+"
        select object on 30 key frame ( for line it looks as "- - - - -" line)
        press << to return to prev keyframe
        select same object on KF 1 ( for line it looks as "- - - - -" line)
        press "merge shapes/tracks" - it will finish merge procedure
    - in object on right sidebar:
        change "Details" to valid value
        press > to move on next frame: the object should be not visible
        press "Switch outside property": the object should be visible again
        it enables interpolation of the object ( tracking ) on all frames between keyframes ( 1 & 30 in our ex )
Check
    - return to last keyframe (30) and check ( first time ) prev frame than object is marked and visible
    
Mark and Track next visible object and Check

#### Save your jab

press "Save" button on upper bar

#### If job was done

Save & Dump results by press Menu -> "Dump annotation" -> "CVAT for video 1.1"
Should be dumped annotation.xml file
File inside must have tracks with all types & attributes you marked
```
<?xml version="1.0" encoding="utf-8"?>
<annotations>
  <version>1.1</version>
  <meta...>
  <track id="0" label="boundary line" source="manual"...>
  ...
  <track id="1" label="Line" source="manual"...>
  ...
  <track id="3" label="Ellipse" source="manual"...>
</annotations>
```
Issue: to many track with Ellipse label
Solution: Ellipse object on different frames should be merged
 
### Appendix
#### Split .mp4 video with ffmpeg

```
ffmpeg -i <filename_.mp4> -ss <start_time> -to <stop time> -c copy <filename_11200_61200>
```