# pytrackmate

[release-badge]: https://img.shields.io/github/v/release/hadim/pytrackmate?logo=github
[test-badge]: https://github.com/hadim/pytrackmate/actions/workflows/test.yaml/badge.svg?branch=main
[lint-badge]: https://github.com/hadim/pytrackmate/actions/workflows/lint.yaml/badge.svg?branch=main

[![GitHub Release][release-badge]](https://github.com/hadim/pytrackmate/releases)
[![Test CI][test-badge]](https://github.com/hadim/pytrackmate/actions/workflows/test.yaml)
[![Lint CI][lint-badge]](https://github.com/hadim/pytrackmate/actions/workflows/lint.yaml)

Import [Trackmate](https://imagej.net/TrackMate) XML files in Python as Pandas dataframe.

## Usage 🚀

Check the [notebook](notebooks/Trackmate.ipynb).

```python
fname = "FakeTracks.xml"
spots = trackmate_peak_import(fname)
```

`spots` is a dataframe with the following columns:

- `t_stamp`
- `t`
- `x`
- `y`
- `z`
- `w`
- `q`
- `spot_id`
- `mean_intensity`
- `median_intensity`
- `min_intensity`
- `max_intensity`
- `total_intensity`
- `std_intensity`
- `contrast`
- `snr`
- `label`

## Installation 📦

```bash
# Pip
pip install pytrackmate

# Conda (mamba and micromamba)
conda install -c conda-forge pytrackmate

# Pixi
pixi add pytrackmate
```

## Development 🛠️

You need to use [pixi](https://pixi.sh).

```bash
# Run tests
pixi run -e dev test

# Lint (ruff)
pixi run -e dev lint

# Format code (ruff)
pixi run -e dev format
```

## Release 🚢

The package is released on [PyPi](https://pypi.org/project/pytrackmate/) and on conda-forge at <https://github.com/conda-forge/pytrackmate-feedstock>.

To cut a new release:

- Trigger [the `release` workflow on the main branch](https://github.com/hadim/pytrackmate/actions/workflows/release.yaml).
- A new GitHub Release will be created with the new version.
- The conda-forge bot will create a PR to update the [feedstock](https://github.com/conda-forge/pytrackmate-feedstock).
- Once the conda-forge PR merged, the new conda version will be available.
