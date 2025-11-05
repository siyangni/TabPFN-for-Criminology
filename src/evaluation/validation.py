"""Validation strategies for model evaluation."""

from typing import Generator, List, Tuple, Optional
import numpy as np
import pandas as pd
from sklearn.model_selection import (
    StratifiedKFold,
    KFold,
    GroupKFold,
    train_test_split,
)
import logging

logger = logging.getLogger(__name__)


class NestedCV:
    """Nested cross-validation for hyperparameter tuning and evaluation."""

    def __init__(
        self,
        outer_cv: int = 5,
        inner_cv: int = 3,
        stratified: bool = True,
        random_state: int = 42,
    ):
        """
        Initialize nested CV.

        Args:
            outer_cv: Number of outer CV folds (for evaluation)
            inner_cv: Number of inner CV folds (for hyperparameter tuning)
            stratified: Whether to use stratified splits
            random_state: Random seed
        """
        self.outer_cv = outer_cv
        self.inner_cv = inner_cv
        self.stratified = stratified
        self.random_state = random_state

    def split(
        self, X: np.ndarray, y: np.ndarray
    ) -> Generator[Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]], None, None]:
        """
        Generate nested CV splits.

        Args:
            X: Features
            y: Target

        Yields:
            Tuple of ((train_indices, val_indices), test_indices) for each outer fold
        """
        # Outer CV splitter
        if self.stratified:
            outer_splitter = StratifiedKFold(
                n_splits=self.outer_cv, shuffle=True, random_state=self.random_state
            )
        else:
            outer_splitter = KFold(
                n_splits=self.outer_cv, shuffle=True, random_state=self.random_state
            )

        # Inner CV splitter
        if self.stratified:
            inner_splitter = StratifiedKFold(
                n_splits=self.inner_cv, shuffle=True, random_state=self.random_state
            )
        else:
            inner_splitter = KFold(
                n_splits=self.inner_cv, shuffle=True, random_state=self.random_state
            )

        for fold_idx, (train_val_idx, test_idx) in enumerate(outer_splitter.split(X, y)):
            logger.info(f"Outer fold {fold_idx + 1}/{self.outer_cv}")

            X_train_val = X[train_val_idx]
            y_train_val = y[train_val_idx]

            # Inner CV for hyperparameter tuning
            inner_splits = list(inner_splitter.split(X_train_val, y_train_val))

            yield (train_val_idx, inner_splits), test_idx


class TemporalValidation:
    """Temporal validation for time-series data."""

    def __init__(
        self,
        test_size: float = 0.2,
        gap: int = 0,
    ):
        """
        Initialize temporal validation.

        Args:
            test_size: Proportion of data for test set
            gap: Gap between train and test (number of time units)
        """
        self.test_size = test_size
        self.gap = gap

    def split(
        self, X: pd.DataFrame, y: pd.Series, time_col: str
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Split data temporally.

        Args:
            X: Features (must include time column)
            y: Target
            time_col: Name of time column

        Returns:
            Tuple of (train_indices, test_indices)
        """
        if time_col not in X.columns:
            raise ValueError(f"Time column '{time_col}' not found in features")

        # Sort by time
        sort_idx = X[time_col].argsort()
        X_sorted = X.iloc[sort_idx]
        y_sorted = y.iloc[sort_idx]

        # Split point
        n_samples = len(X_sorted)
        split_point = int(n_samples * (1 - self.test_size))

        # Apply gap
        split_point_with_gap = split_point - self.gap

        train_idx = sort_idx[:split_point_with_gap]
        test_idx = sort_idx[split_point:]

        logger.info(
            f"Temporal split: {len(train_idx)} train, {len(test_idx)} test, gap={self.gap}"
        )

        return train_idx, test_idx


class JurisdictionalHoldout:
    """Holdout validation across jurisdictions/sites."""

    def __init__(
        self,
        test_fraction: float = 0.2,
        random_state: int = 42,
    ):
        """
        Initialize jurisdictional holdout.

        Args:
            test_fraction: Fraction of jurisdictions for test
            random_state: Random seed
        """
        self.test_fraction = test_fraction
        self.random_state = random_state

    def split(
        self, X: pd.DataFrame, y: pd.Series, jurisdiction_col: str
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Split data by jurisdiction.

        Args:
            X: Features (must include jurisdiction column)
            y: Target
            jurisdiction_col: Name of jurisdiction column

        Returns:
            Tuple of (train_indices, test_indices)
        """
        if jurisdiction_col not in X.columns:
            raise ValueError(
                f"Jurisdiction column '{jurisdiction_col}' not found in features"
            )

        # Get unique jurisdictions
        jurisdictions = X[jurisdiction_col].unique()

        # Sample test jurisdictions
        n_test = max(1, int(len(jurisdictions) * self.test_fraction))

        np.random.seed(self.random_state)
        test_jurisdictions = np.random.choice(
            jurisdictions, size=n_test, replace=False
        )

        # Split indices
        test_mask = X[jurisdiction_col].isin(test_jurisdictions)
        train_idx = np.where(~test_mask)[0]
        test_idx = np.where(test_mask)[0]

        logger.info(
            f"Jurisdictional split: {len(train_idx)} train samples "
            f"from {len(jurisdictions) - n_test} jurisdictions, "
            f"{len(test_idx)} test samples from {n_test} jurisdictions"
        )

        return train_idx, test_idx


class SpatialGroupKFold:
    """Spatial K-fold cross-validation using geographic groups."""

    def __init__(
        self,
        n_splits: int = 5,
        random_state: int = 42,
    ):
        """
        Initialize spatial group K-fold.

        Args:
            n_splits: Number of folds
            random_state: Random seed
        """
        self.n_splits = n_splits
        self.random_state = random_state

    def split(
        self, X: pd.DataFrame, y: pd.Series, group_col: str
    ) -> Generator[Tuple[np.ndarray, np.ndarray], None, None]:
        """
        Generate spatial CV splits.

        Args:
            X: Features (must include group column)
            y: Target
            group_col: Name of group column (e.g., state, county)

        Yields:
            Tuple of (train_indices, test_indices) for each fold
        """
        if group_col not in X.columns:
            raise ValueError(f"Group column '{group_col}' not found in features")

        groups = X[group_col]

        # Use sklearn's GroupKFold
        gkf = GroupKFold(n_splits=self.n_splits)

        for fold_idx, (train_idx, test_idx) in enumerate(gkf.split(X, y, groups)):
            logger.info(f"Spatial fold {fold_idx + 1}/{self.n_splits}")
            yield train_idx, test_idx
