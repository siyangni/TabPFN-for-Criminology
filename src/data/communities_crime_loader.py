"""UCI Communities and Crime dataset loader."""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, List, Tuple
import logging
from ucimlrepo import fetch_ucirepo

from .base_loader import BaseDataLoader, DatasetMetadata

logger = logging.getLogger(__name__)


class CommunitiesCrimeLoader(BaseDataLoader):
    """Loader for UCI Communities and Crime dataset."""

    UCI_ID = 183  # Communities and Crime dataset ID

    def __init__(
        self,
        data_dir: Path,
        random_state: int = 42,
        test_size: float = 0.2,
        val_size: float = 0.1,
        drop_missing_lemas: bool = True,
    ):
        """
        Initialize Communities and Crime loader.

        Args:
            data_dir: Directory for data storage
            random_state: Random seed
            test_size: Test set proportion
            val_size: Validation set proportion
            drop_missing_lemas: Whether to drop rows with missing LEMAS data
        """
        super().__init__(data_dir, random_state, test_size, val_size)
        self.drop_missing_lemas = drop_missing_lemas

        self.raw_dir = self.data_dir / "raw" / "communities_crime"
        self.raw_dir.mkdir(parents=True, exist_ok=True)

    def download(self) -> None:
        """
        Download Communities and Crime data using ucimlrepo.

        The data is downloaded via the ucimlrepo package which handles
        fetching from the UCI ML Repository.
        """
        logger.info(f"Downloading Communities and Crime dataset (ID: {self.UCI_ID})")

        try:
            # Fetch dataset
            dataset = fetch_ucirepo(id=self.UCI_ID)

            # Save raw data
            features_path = self.raw_dir / "features.csv"
            targets_path = self.raw_dir / "targets.csv"
            metadata_path = self.raw_dir / "metadata.txt"

            dataset.data.features.to_csv(features_path, index=False)
            dataset.data.targets.to_csv(targets_path, index=False)

            # Save metadata
            with open(metadata_path, "w") as f:
                f.write(f"Name: {dataset.metadata.name}\n")
                f.write(f"Description: {dataset.metadata.abstract}\n")
                f.write(f"Variables: {dataset.variables}\n")

            logger.info(f"Downloaded and saved to {self.raw_dir}")

        except Exception as e:
            logger.error(f"Error downloading dataset: {e}")
            raise

    def load_raw(self) -> pd.DataFrame:
        """
        Load raw Communities and Crime data.

        Returns:
            Raw dataframe with features and target combined
        """
        features_path = self.raw_dir / "features.csv"
        targets_path = self.raw_dir / "targets.csv"

        if not features_path.exists() or not targets_path.exists():
            logger.info("Raw data not found, downloading...")
            self.download()

        # Load features and targets
        features = pd.read_csv(features_path)
        targets = pd.read_csv(targets_path)

        # Combine features and targets
        df = pd.concat([features, targets], axis=1)

        logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")

        return df

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess Communities and Crime data.

        Args:
            df: Raw dataframe

        Returns:
            Preprocessed dataframe
        """
        logger.info(f"Starting preprocessing with {len(df)} rows")

        # Target variable: ViolentCrimesPerPop
        target_col = "ViolentCrimesPerPop"

        if target_col not in df.columns:
            raise ValueError(f"Target column {target_col} not found in dataset")

        # Remove non-predictive features
        # These are identifiers that shouldn't be used for prediction
        non_predictive = [
            "communityname",
            "state",
            "countyCode",
            "communityCode",
            "fold",
        ]
        df = df.drop(columns=[col for col in non_predictive if col in df.columns])

        # Handle missing values (marked as '?')
        # Replace '?' with NaN
        df = df.replace("?", np.nan)

        # Convert all columns to numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # Check missing data patterns
        missing_pct = (df.isnull().sum() / len(df)) * 100
        logger.info(
            f"Columns with >50% missing: {missing_pct[missing_pct > 50].index.tolist()}"
        )

        # LEMAS columns (law enforcement management) have many missing values
        lemas_cols = [col for col in df.columns if "Lemas" in col or "police" in col]

        if self.drop_missing_lemas:
            # Drop rows with missing LEMAS data
            logger.info(
                f"Dropping {df[lemas_cols].isnull().any(axis=1).sum()} rows with missing LEMAS data"
            )
            df = df.dropna(subset=lemas_cols)
        else:
            # Impute missing LEMAS data with median
            logger.info("Imputing missing LEMAS data with median")
            for col in lemas_cols:
                if df[col].isnull().any():
                    df[col].fillna(df[col].median(), inplace=True)

        # Drop remaining columns with >50% missing
        high_missing_cols = missing_pct[missing_pct > 50].index.tolist()
        if high_missing_cols:
            logger.info(f"Dropping columns with >50% missing: {high_missing_cols}")
            df = df.drop(columns=high_missing_cols)

        # For remaining missing values, use median imputation
        remaining_missing = df.columns[df.isnull().any()].tolist()
        if remaining_missing:
            logger.info(f"Imputing remaining missing values in: {remaining_missing}")
            for col in remaining_missing:
                df[col].fillna(df[col].median(), inplace=True)

        # Remove rows with missing target
        df = df.dropna(subset=[target_col])

        logger.info(f"Final dataset: {len(df)} rows, {len(df.columns)} columns")
        logger.info(f"Target statistics:\n{df[target_col].describe()}")

        return df

    def get_metadata(self) -> DatasetMetadata:
        """
        Get Communities and Crime dataset metadata.

        Returns:
            Dataset metadata object
        """
        # Load a sample to get actual statistics
        try:
            df = self.load_processed("communities_crime")
        except FileNotFoundError:
            df_raw = self.load_raw()
            df = self.preprocess(df_raw)

        target_col = "ViolentCrimesPerPop"

        return DatasetMetadata(
            name="Communities and Crime",
            task_type="regression",
            n_samples=len(df),
            n_features=len(df.columns) - 1,
            n_classes=None,
            target_name=target_col,
            sensitive_features=["racepctblack", "racePctWhite", "racePctAsian", "racePctHisp"],
            feature_names=[col for col in df.columns if col != target_col],
            class_names=None,
            source="UCI Machine Learning Repository",
            license="Creative Commons Attribution 4.0",
            description=(
                "Communities and Crime dataset from UCI. "
                "Combines socio-economic data from 1990 US Census, "
                "law enforcement data from 1990 Law Enforcement Management "
                "and Administrative Statistics survey, and crime data from "
                "the 1995 FBI UCR. Target: violent crimes per 100K population."
            ),
        )

    def get_X_y_sensitive(
        self, df: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
        """
        Split dataframe into features, target, and sensitive attributes.

        Args:
            df: Preprocessed dataframe

        Returns:
            Tuple of (features, target, sensitive_attributes)
        """
        target_col = "ViolentCrimesPerPop"

        # Racial composition features as sensitive attributes
        sensitive_cols = [
            col
            for col in ["racepctblack", "racePctWhite", "racePctAsian", "racePctHisp"]
            if col in df.columns
        ]

        X = df.drop(columns=[target_col] + sensitive_cols)
        y = df[target_col]
        sensitive = df[sensitive_cols] if sensitive_cols else pd.DataFrame()

        return X, y, sensitive

    def prepare_for_modeling(
        self, df: pd.DataFrame, include_race_features: bool = True
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Prepare data for modeling.

        Args:
            df: Preprocessed dataframe
            include_race_features: Whether to include racial composition features

        Returns:
            Tuple of (features, target)
        """
        target_col = "ViolentCrimesPerPop"

        X = df.drop(columns=[target_col])
        y = df[target_col]

        if not include_race_features:
            # Remove racial composition features for fairness-only prediction
            race_cols = [
                col
                for col in X.columns
                if any(
                    keyword in col.lower()
                    for keyword in ["race", "ethnic", "immigrant", "foreign"]
                )
            ]
            if race_cols:
                logger.info(f"Removing race-related features: {race_cols}")
                X = X.drop(columns=race_cols)

        return X, y

    def load_and_prepare(
        self, include_race_features: bool = True, force_download: bool = False
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Convenience method to load, preprocess, and prepare data.

        Args:
            include_race_features: Whether to include racial composition features
            force_download: Whether to force re-download

        Returns:
            Tuple of (features, target)
        """
        if force_download:
            self.download()

        # Try to load processed data
        try:
            df = self.load_processed("communities_crime")
            logger.info("Loaded preprocessed data from cache")
        except FileNotFoundError:
            df_raw = self.load_raw()
            df = self.preprocess(df_raw)
            self.save_processed(df, "communities_crime")
            logger.info("Preprocessed and cached data")

        return self.prepare_for_modeling(df, include_race_features)

    def get_state_groups(self, df: pd.DataFrame) -> pd.Series:
        """
        Get state groupings for spatial cross-validation.

        Note: State information is in the raw data but removed during preprocessing.
        This method requires the raw dataframe.

        Args:
            df: Raw dataframe (before preprocessing)

        Returns:
            Series of state codes
        """
        if "state" in df.columns:
            return df["state"]
        else:
            logger.warning(
                "State column not found. Load raw data to get state groups."
            )
            return None
