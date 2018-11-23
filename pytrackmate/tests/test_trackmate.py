import os

from pytrackmate import trackmate_peak_import


def test_import():
    fname = os.path.join(os.path.dirname(__file__), "FakeTracks.xml")
    spots = trackmate_peak_import(fname)
    assert spots.shape == (12, 17)
