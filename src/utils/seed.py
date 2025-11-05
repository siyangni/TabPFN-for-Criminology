"""Deterministic seed management for reproducibility."""

import os
import random
import numpy as np
import torch


def set_seed(seed: int = 42) -> None:
    """
    Set random seeds for reproducibility across all libraries.

    Args:
        seed: Random seed value (default: 42)
    """
    # Python random
    random.seed(seed)

    # NumPy
    np.random.seed(seed)

    # PyTorch
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

    # PyTorch deterministic operations
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    # Python hash seed
    os.environ["PYTHONHASHSEED"] = str(seed)

    # Lightning
    try:
        from lightning import seed_everything
        seed_everything(seed, workers=True)
    except ImportError:
        pass


def get_seed() -> int:
    """
    Get the current random seed from environment or use default.

    Returns:
        Random seed value
    """
    return int(os.environ.get("RANDOM_SEED", 42))
