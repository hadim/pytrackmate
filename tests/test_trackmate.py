import pathlib

from pytrackmate import trackmate_peak_import


def test_import():
    fname = pathlib.Path(__file__).parent / "FakeTracks.xml"
    spots = trackmate_peak_import(fname)
    assert spots.shape == (12, 17)

    assert spots.columns.to_list() == [
        "t_stamp",
        "t",
        "x",
        "y",
        "z",
        "w",
        "q",
        "spot_id",
        "mean_intensity",
        "median_intensity",
        "min_intensity",
        "max_intensity",
        "total_intensity",
        "std_intensity",
        "contrast",
        "snr",
        "label",
    ]

    assert spots.iloc[0].to_list() == [
        0.0,
        0.0,
        28.81291282851087,
        5.666830103137038,
        0.0,
        2.0000000141168894,
        7.669281005859375,
        35.0,
        50.22680412371134,
        28.0,
        0.0,
        248.0,
        4872.0,
        58.9290719768688,
        0.2350598400953469,
        0.32443401070344374,
        0.0,
    ]
