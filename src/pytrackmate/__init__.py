import importlib.metadata

from ._trackmate import trackmate_peak_import

__version__ = importlib.metadata.version("pytrackmate")

__all__ = ["trackmate_peak_import", "__version__"]
