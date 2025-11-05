"""Base data loader class for all datasets."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


@dataclass
class DatasetMetadata:
    """Metadata for a dataset."""

    name: str
    task_type: str  # "classification" or "regression"
    n_samples: int
    n_features: int
    n_classes: Optional[int]
    target_name: str
    sensitive_features: List[str]
    feature_names: List[str]
    class_names: Optional[List[str]]
    source: str
    license: str
    description: str


class BaseDataLoader(ABC):
    """Base class for all data loaders."""

    def __init__(
        self,
        data_dir: Path,
        random_state: int = 42,
        test_size: float = 0.2,
        val_size: float = 0.1,
    ):
        """
        Initialize data loader.

        Args:
            data_dir: Directory containing data files
            random_state: Random seed for reproducibility
            test_size: Proportion of data for test set
            val_size: Proportion of training data for validation set
        """
        self.data_dir = Path(data_dir)
        self.random_state = random_state
        self.test_size = test_size
        self.val_size = val_size

        self.data_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def download(self) -> None:
        """Download raw data."""
        pass

    @abstractmethod
    def load_raw(self) -> pd.DataFrame:
        """Load raw data into DataFrame."""
        pass

    @abstractmethod
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """Preprocess raw data."""
        pass

    @abstractmethod
    def get_metadata(self) -> DatasetMetadata:
        """Get dataset metadata."""
        pass

    def get_X_y(
        self, df: pd.DataFrame, target_col: str
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Split dataframe into features and target.

        Args:
            df: DataFrame with features and target
            target_col: Name of target column

        Returns:
            Tuple of (features, target)
        """
        X = df.drop(columns=[target_col])
        y = df[target_col]
        return X, y

    def train_test_split(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        stratify: bool = True,
        group_col: Optional[str] = None,
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """
        Split data into train and test sets.

        Args:
            X: Features
            y: Target
            stratify: Whether to stratify by target
            group_col: Optional column name for grouped splitting

        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
        """
        stratify_col = y if stratify else None

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=self.test_size,
            random_state=self.random_state,
            stratify=stratify_col,
        )

        return X_train, X_test, y_train, y_test

    def get_train_val_test_split(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        stratify: bool = True,
    ) -> Tuple[
        pd.DataFrame,
        pd.DataFrame,
        pd.DataFrame,
        pd.Series,
        pd.Series,
        pd.Series,
    ]:
        """
        Split data into train, validation, and test sets.

        Args:
            X: Features
            y: Target
            stratify: Whether to stratify by target

        Returns:
            Tuple of (X_train, X_val, X_test, y_train, y_val, y_test)
        """
        # First split: train+val vs test
        X_trainval, X_test, y_trainval, y_test = self.train_test_split(
            X, y, stratify=stratify
        )

        # Second split: train vs val
        stratify_col = y_trainval if stratify else None
        val_size_adjusted = self.val_size / (1 - self.test_size)

        X_train, X_val, y_train, y_val = train_test_split(
            X_trainval,
            y_trainval,
            test_size=val_size_adjusted,
            random_state=self.random_state,
            stratify=stratify_col,
        )

        return X_train, X_val, X_test, y_train, y_val, y_test

    def save_processed(self, df: pd.DataFrame, filename: str) -> None:
        """
        Save processed data to parquet file.

        Args:
            df: Processed dataframe
            filename: Output filename (without extension)
        """
        output_path = self.data_dir / "processed" / f"{filename}.parquet"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(output_path, index=False)

    def load_processed(self, filename: str) -> pd.DataFrame:
        """
        Load processed data from parquet file.

        Args:
            filename: Input filename (without extension)

        Returns:
            Processed dataframe
        """
        input_path = self.data_dir / "processed" / f"{filename}.parquet"
        return pd.read_parquet(input_path)

    def describe(self) -> Dict[str, Any]:
        """
        Get descriptive statistics about the dataset.

        Returns:
            Dictionary with dataset statistics
        """
        metadata = self.get_metadata()

        return {
            "name": metadata.name,
            "task_type": metadata.task_type,
            "n_samples": metadata.n_samples,
            "n_features": metadata.n_features,
            "n_classes": metadata.n_classes,
            "target": metadata.target_name,
            "sensitive_features": metadata.sensitive_features,
            "source": metadata.source,
        }
