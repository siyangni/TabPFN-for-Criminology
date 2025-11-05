"""Configuration management utilities."""

import yaml
from pathlib import Path
from typing import Dict, Any
from omegaconf import OmegaConf, DictConfig


def load_config(config_path: Path) -> DictConfig:
    """
    Load configuration from YAML file using OmegaConf.

    Args:
        config_path: Path to YAML config file

    Returns:
        Configuration as DictConfig
    """
    config = OmegaConf.load(config_path)
    return config


def save_config(config: DictConfig, output_path: Path) -> None:
    """
    Save configuration to YAML file.

    Args:
        config: Configuration object
        output_path: Path to save YAML file
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    OmegaConf.save(config, output_path)


def merge_configs(*configs: DictConfig) -> DictConfig:
    """
    Merge multiple configurations (later configs override earlier ones).

    Args:
        *configs: Variable number of DictConfig objects

    Returns:
        Merged configuration
    """
    return OmegaConf.merge(*configs)


def config_to_dict(config: DictConfig) -> Dict[str, Any]:
    """
    Convert OmegaConf DictConfig to plain Python dict.

    Args:
        config: Configuration object

    Returns:
        Plain Python dictionary
    """
    return OmegaConf.to_container(config, resolve=True)
