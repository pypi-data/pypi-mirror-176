"""Core module.

Contains pandas-based model classes
"""

from __future__ import annotations

from .basedatasetmodel import BaseDatasetModel
from .pandasmodel import PandasModel
from .pandasindexmodel import PandasIndexModel

__all__ = [
    "BaseDatasetModel",
    "PandasModel",
    "PandasIndexModel",
]
