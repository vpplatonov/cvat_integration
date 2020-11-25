import json
import xmltodict


def get_label(track):
    label = track["@label"]
    label_shape_type = [key for key in track.keys() if not key.startswith("@")]
    if label_shape_type:
        label_shape_type = label_shape_type[0]
    else:
        return None, None

    return label, label_shape_type


def merge_same_object_tracks(track, new_tracks):
    """
    :param: track
    :param: new_tracks

    Main assumption: there are ony one object same type-attribute on frames
    """
    label, label_shape_type = get_label(track)

    if label in new_tracks and \
            (track[label_shape_type][0]["attribute"]["#text"] in new_tracks[label]
             if "attribute" in track[label_shape_type][0] else True):
        if "attribute" in track[label_shape_type][0]:
            if new_tracks[label][track[label_shape_type][0]["attribute"]["#text"]][label_shape_type][0]["@frame"] \
                    < track[label_shape_type][0]["@frame"]:
                new_tracks[label][track[label_shape_type][0]["attribute"]["#text"]][label_shape_type] = \
                    new_tracks[label][track[label_shape_type][0]["attribute"]["#text"]][label_shape_type] + \
                    track[label_shape_type]
            else:
                new_tracks[label][track[label_shape_type][0]["attribute"]["#text"]][label_shape_type] = \
                    track[label_shape_type] + \
                    new_tracks[label][track[label_shape_type][0]["attribute"]["#text"]][label_shape_type]
        else:
            if new_tracks[label][label_shape_type][0]["@frame"] < track[label_shape_type][0]["@frame"]:
                new_tracks[label][label_shape_type] = \
                    new_tracks[label][label_shape_type] + track[label_shape_type]
            else:
                new_tracks[label][label_shape_type] = \
                    track[label_shape_type] + new_tracks[label][label_shape_type]
    else:
        if "attribute" in track[label_shape_type][0]:
            try:
                new_tracks[label][track[label_shape_type][0]["attribute"]["#text"]] = track
            except KeyError as e:
                new_tracks[label] = {}
                new_tracks[label][track[label_shape_type][0]["attribute"]["#text"]] = track
        else:
            new_tracks[label] = track


if __name__ == "__main__":
    """
    Merge the same object annotated in CVAT for video 1.1
    after auto annotation or messed merge by hands
    Assumption: the annotated object present in frames only ones
    """
    file = '../dumps/gt_cvat_for_video_1.1/annotations'
    extensions = '.xml'
    with open(file + extensions) as fd:
        doc = xmltodict.parse(fd.read())

    print(f'file {file} uploaded')

    labels = doc["annotations"]['meta']["task"]["labels"]
    new_tracks = {}
    removed_tracks = []

    for i, track in enumerate(doc["annotations"]["track"]):
        merge_same_object_tracks(track, new_tracks)
        removed_tracks.append(i)

    for i in reversed(removed_tracks):
        del doc["annotations"]["track"][i]

    for label in new_tracks.keys():
        if any(key.startswith("@") for key in new_tracks[label].keys()):
            doc["annotations"]["track"].append(new_tracks[label])
        else:
            for attribute in new_tracks[label].keys():
                doc["annotations"]["track"].append(new_tracks[label][attribute])

    with open(file + '.json', 'w') as fd:
        json.dump(doc, fd)
