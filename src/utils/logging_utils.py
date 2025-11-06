"""Logging utilities for experiment tracking."""

import logging
import sys
from pathlib import Path
from typing import Optional
import json
from datetime import datetime


def setup_logger(
    name: str = "tabpfn_criminology",
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
) -> logging.Logger:
    """
    Set up a logger with console and optional file handlers.

    Args:
        name: Logger name
        level: Logging level
        log_file: Optional path to log file

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers
    logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(console_formatter)
        logger.addHandler(file_handler)

    return logger


def log_versions(logger: Optional[logging.Logger] = None) -> dict:
    """
    Log versions of key packages for reproducibility.

    Args:
        logger: Optional logger instance

    Returns:
        Dictionary of package versions
    """
    import platform
    import numpy
    import pandas
    import sklearn

    versions = {
        "timestamp": datetime.now().isoformat(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "numpy": numpy.__version__,
        "pandas": pandas.__version__,
        "scikit-learn": sklearn.__version__,
    }

    # Optional PyTorch
    try:
        import torch
        versions["torch"] = torch.__version__
        versions["cuda_available"] = torch.cuda.is_available()
        versions["cuda_version"] = torch.version.cuda if torch.cuda.is_available() else None
    except (ImportError, OSError):
        versions["torch"] = "not installed"
        versions["cuda_available"] = False
        versions["cuda_version"] = None

    # Optional packages
    optional_packages = [
        "tabpfn",
        "xgboost",
        "lightgbm",
        "catboost",
        "fairlearn",
        "aequitas",
        "shap",
        "optuna",
        "lightning",
        "torchmetrics",
    ]

    for package_name in optional_packages:
        try:
            module = __import__(package_name)
            versions[package_name] = getattr(module, "__version__", "unknown")
        except ImportError:
            versions[package_name] = "not installed"

    if logger:
        logger.info("Package versions:")
        for key, value in versions.items():
            logger.info(f"  {key}: {value}")

    return versions


def save_versions(output_path: Path) -> None:
    """
    Save package versions to a JSON file.

    Args:
        output_path: Path to save versions JSON
    """
    versions = log_versions()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(versions, f, indent=2)
