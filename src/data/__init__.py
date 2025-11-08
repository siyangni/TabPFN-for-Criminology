"""Data loading and preprocessing modules."""

from .base_loader import BaseDataLoader
from .compas_loader import COMPASLoader
from .communities_crime_loader import CommunitiesCrimeLoader
from .ncvs_loader import NCVSLoader
from .fbi_ucr_loader import FBIUCRLoader

# Backward compatibility alias for notebooks
COMPASDataLoader = COMPASLoader

__all__ = [
    "BaseDataLoader",
    "COMPASLoader",
    "COMPASDataLoader",  # Alias
    "CommunitiesCrimeLoader",
    "NCVSLoader",
    "FBIUCRLoader",
]
