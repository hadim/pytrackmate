import xml.etree.cElementTree as et
import os

import numpy as np
import pandas as pd


def _safe_find(element: et.Element, tag: str) -> et.Element:
    """Safely find a child element, raising ValueError if not found."""
    found = element.find(tag)
    if found is None:
        raise ValueError(f"No '{tag}' tag found in the XML file.")
    return found


def _safe_get(element: et.Element, attribute: str) -> str:
    """Safely get an attribute from an element, raising ValueError if not found."""
    value = element.get(attribute)
    if value is None:
        raise ValueError(f"No attribute '{attribute}' found in the XML element.")
    return value


def trackmate_peak_import(
    trackmate_xml_path: str | os.PathLike,
    get_tracks: bool = False,
) -> pd.DataFrame:
    """Import detected peaks with TrackMate Fiji plugin."""

    with open(trackmate_xml_path, "r") as f:
        xml_string = f.read()
    root = et.fromstring(xml_string)

    object_labels = {
        "FRAME": "t_stamp",
        "POSITION_T": "t",
        "POSITION_X": "x",
        "POSITION_Y": "y",
        "POSITION_Z": "z",
        "ESTIMATED_DIAMETER": "w",
        "QUALITY": "q",
        "ID": "spot_id",
        "MEAN_INTENSITY": "mean_intensity",
        "MEDIAN_INTENSITY": "median_intensity",
        "MIN_INTENSITY": "min_intensity",
        "MAX_INTENSITY": "max_intensity",
        "TOTAL_INTENSITY": "total_intensity",
        "STANDARD_DEVIATION": "std_intensity",
        "CONTRAST": "contrast",
        "SNR": "snr",
    }

    model = _safe_find(root, "Model")
    feature_declarations = _safe_find(model, "FeatureDeclarations")
    spot_features = _safe_find(feature_declarations, "SpotFeatures")

    features = [c.get("feature") for c in list(spot_features)] + ["ID"]

    all_spots = _safe_find(model, "AllSpots")

    objects = []
    for frame in all_spots.findall("SpotsInFrame"):
        for spot in frame.findall("Spot"):
            single_object = []
            for label in features:
                if label is None:
                    raise ValueError(
                        f"Attribute '{label}' is missing in the XML spot element."
                    )

                value = spot.get(label)
                if value is None:
                    raise ValueError(
                        f"Attribute '{label}' is missing in the XML spot element."
                    )

                single_object.append(value)
            objects.append(single_object)

    trajs = pd.DataFrame(objects, columns=features)
    trajs = trajs.astype(float)

    # Apply initial filtering
    settings = _safe_find(root, "Settings")
    initial_filter = _safe_find(settings, "InitialSpotFilter")

    trajs = filter_spots(
        trajs,
        name=_safe_get(initial_filter, "feature"),
        value=float(_safe_get(initial_filter, "value")),
        isabove=_safe_get(initial_filter, "isabove") == "true",
    )

    # Apply filters
    spot_filters = _safe_find(settings, "SpotFilterCollection")

    for spot_filter in spot_filters.findall("Filter"):
        trajs = filter_spots(
            trajs,
            name=_safe_get(spot_filter, "feature"),
            value=float(_safe_get(spot_filter, "value")),
            isabove=_safe_get(spot_filter, "isabove") == "true",
        )

    trajs = trajs.reindex(columns=list(object_labels.keys()))
    trajs.columns = [object_labels[k] for k in object_labels.keys()]
    trajs["label"] = np.arange(trajs.shape[0])

    # Get tracks
    if get_tracks:
        filtered_track_ids = [
            int(_safe_get(track, "TRACK_ID"))
            for track in _safe_find(model, "FilteredTracks").findall("TrackID")
        ]

        label_id = 0
        trajs["label"] = np.nan

        all_tracks = _safe_find(model, "AllTracks")

        for track in all_tracks.findall("Track"):
            track_id = int(_safe_get(track, "TRACK_ID"))
            if track_id in filtered_track_ids:
                spot_ids = [
                    (
                        edge.get("SPOT_SOURCE_ID"),
                        edge.get("SPOT_TARGET_ID"),
                        edge.get("EDGE_TIME"),
                    )
                    for edge in track.findall("Edge")
                ]
                spot_ids = np.array(spot_ids).astype("float")[:, :2]
                spot_ids = set(spot_ids.flatten())

                trajs.loc[trajs["spot_id"].isin(spot_ids), "label"] = label_id
                label_id += 1

        # Label remaining columns
        single_track = trajs.loc[trajs["label"].isnull()]
        trajs.loc[trajs["label"].isnull(), "label"] = label_id + np.arange(
            0, len(single_track)
        )

    return trajs


def filter_spots(
    spots: pd.DataFrame, name: str, value: float, isabove: bool
) -> pd.DataFrame:
    """Filter spots based on a given feature."""
    if name not in spots.columns:
        raise ValueError(f"Feature '{name}' does not exist in the spots DataFrame.")

    if isabove:
        spots = spots[spots[name] > value]
    else:
        spots = spots[spots[name] < value]

    return spots
