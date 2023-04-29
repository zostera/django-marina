__all__ = [
    "__version__",
]


# TODO: Remove after Python 3.7 support gets dropped (py37)
try:
    import importlib.metadata as importlib_metadata
except ImportError:
    import importlib_metadata as importlib_metadata

__version__ = importlib_metadata.version(__package__ or __name__)
