"""COMPAS dataset loader and preprocessor."""

import requests
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Tuple
import logging

from .base_loader import BaseDataLoader, DatasetMetadata

logger = logging.getLogger(__name__)


class COMPASLoader(BaseDataLoader):
    """Loader for COMPAS recidivism dataset from ProPublica."""

    COMPAS_URL_BASE = "https://raw.githubusercontent.com/propublica/compas-analysis/master/"
    COMPAS_FILES = {
        "two_year": "compas-scores-two-years.csv",
        "two_year_violent": "compas-scores-two-years-violent.csv",
        "raw": "compas-scores-raw.csv",
    }

    def __init__(
        self,
        data_dir: Path,
        task: str = "two_year",  # "two_year" or "two_year_violent"
        random_state: int = 42,
        test_size: float = 0.2,
        val_size: float = 0.1,
    ):
        """
        Initialize COMPAS loader.

        Args:
            data_dir: Directory for data storage
            task: Prediction task ("two_year" for general recidivism,
                  "two_year_violent" for violent recidivism)
            random_state: Random seed
            test_size: Test set proportion
            val_size: Validation set proportion
        """
        super().__init__(data_dir, random_state, test_size, val_size)
        self.task = task

        if task not in self.COMPAS_FILES:
            raise ValueError(
                f"Task must be one of {list(self.COMPAS_FILES.keys())}, got {task}"
            )

        self.raw_dir = self.data_dir / "raw" / "compas"
        self.raw_dir.mkdir(parents=True, exist_ok=True)

    def download(self) -> None:
        """Download COMPAS data from ProPublica repository."""
        for name, filename in self.COMPAS_FILES.items():
            url = self.COMPAS_URL_BASE + filename
            output_path = self.raw_dir / filename

            if output_path.exists():
                logger.info(f"File {filename} already exists, skipping download")
                continue

            logger.info(f"Downloading {filename} from {url}")
            response = requests.get(url)
            response.raise_for_status()

            with open(output_path, "wb") as f:
                f.write(response.content)

            logger.info(f"Saved to {output_path}")

    def load_raw(self) -> pd.DataFrame:
        """
        Load raw COMPAS data.

        Returns:
            Raw dataframe
        """
        filename = self.COMPAS_FILES[self.task]
        file_path = self.raw_dir / filename

        if not file_path.exists():
            logger.info(f"File not found, downloading...")
            self.download()

        df = pd.read_csv(file_path)
        logger.info(f"Loaded {len(df)} rows from {file_path}")

        return df

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess COMPAS data following ProPublica methodology.

        This follows the filtering and preprocessing steps from ProPublica's
        original analysis to ensure consistency with published results.

        Args:
            df: Raw dataframe

        Returns:
            Preprocessed dataframe
        """
        logger.info(f"Starting preprocessing with {len(df)} rows")

        # ProPublica filtering criteria
        # 1. Remove rows with missing days_b_screening_arrest
        df = df[df["days_b_screening_arrest"] <= 30]
        df = df[df["days_b_screening_arrest"] >= -30]

        # 2. Remove rows with is_recid == -1 (invalid)
        df = df[df["is_recid"] != -1]

        # 3. Filter by charge degree (only felonies and misdemeanors)
        df = df[df["c_charge_degree"].isin(["F", "M"])]

        # 4. Filter out rows with COMPAS screening date not within 30 days of arrest
        df = df[df["score_text"] != "N/A"]

        logger.info(f"After ProPublica filtering: {len(df)} rows")

        # Select target variable based on task
        if self.task == "two_year":
            target_col = "two_year_recid"
        elif self.task == "two_year_violent":
            target_col = "two_year_violent_recid"
        else:
            raise ValueError(f"Unknown task: {self.task}")

        # Select features
        feature_cols = [
            # Demographics
            "age",
            "age_cat",
            "sex",
            "race",
            # Criminal history
            "juv_fel_count",
            "juv_misd_count",
            "juv_other_count",
            "priors_count",
            "c_charge_degree",
            # COMPAS scores (optional - can be excluded for fairness-only prediction)
            "decile_score",
            "score_text",
        ]

        # Keep only relevant columns
        cols_to_keep = feature_cols + [target_col]
        df = df[cols_to_keep].copy()

        # Handle missing values
        df = df.dropna(subset=[target_col])

        # Encode categorical variables
        df["age_cat"] = df["age_cat"].astype("category")
        df["sex"] = df["sex"].astype("category")
        df["race"] = df["race"].astype("category")
        df["c_charge_degree"] = df["c_charge_degree"].astype("category")
        df["score_text"] = df["score_text"].astype("category")

        # Ensure target is binary
        df[target_col] = df[target_col].astype(int)

        logger.info(f"Final dataset: {len(df)} rows, {len(df.columns)} columns")
        logger.info(f"Class distribution:\n{df[target_col].value_counts()}")

        return df

    def get_metadata(self) -> DatasetMetadata:
        """
        Get COMPAS dataset metadata.

        Returns:
            Dataset metadata object
        """
        # Load a sample to get actual statistics
        try:
            df = self.load_processed(f"compas_{self.task}")
        except FileNotFoundError:
            # If processed data doesn't exist, load and preprocess
            df_raw = self.load_raw()
            df = self.preprocess(df_raw)

        target_col = (
            "two_year_recid"
            if self.task == "two_year"
            else "two_year_violent_recid"
        )

        return DatasetMetadata(
            name=f"COMPAS ({self.task})",
            task_type="classification",
            n_samples=len(df),
            n_features=len(df.columns) - 1,
            n_classes=2,
            target_name=target_col,
            sensitive_features=["race", "sex", "age_cat"],
            feature_names=[col for col in df.columns if col != target_col],
            class_names=["No Recidivism", "Recidivism"],
            source="ProPublica COMPAS Analysis",
            license="Creative Commons (ProPublica)",
            description=(
                f"COMPAS recidivism prediction task ({self.task}). "
                "Defendants from Broward County, Florida (2013-2014). "
                "Target: recidivism within two years of screening."
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
        target_col = (
            "two_year_recid"
            if self.task == "two_year"
            else "two_year_violent_recid"
        )
        sensitive_cols = ["race", "sex", "age_cat"]

        X = df.drop(columns=[target_col] + sensitive_cols)
        y = df[target_col]
        sensitive = df[sensitive_cols]

        return X, y, sensitive

    def prepare_for_modeling(
        self, df: pd.DataFrame, include_compas_score: bool = False
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Prepare data for modeling with appropriate encoding.

        Args:
            df: Preprocessed dataframe
            include_compas_score: Whether to include COMPAS risk scores as features

        Returns:
            Tuple of (encoded_features, target)
        """
        target_col = (
            "two_year_recid"
            if self.task == "two_year"
            else "two_year_violent_recid"
        )

        # Separate features and target
        X = df.drop(columns=[target_col])
        y = df[target_col]

        # Optionally remove COMPAS scores (for fairness-only prediction)
        if not include_compas_score:
            X = X.drop(columns=["decile_score", "score_text"], errors="ignore")

        # One-hot encode categorical variables
        categorical_cols = X.select_dtypes(include=["category", "object"]).columns
        X_encoded = pd.get_dummies(X, columns=categorical_cols, drop_first=True)

        return X_encoded, y

    def load_and_prepare(
        self, include_compas_score: bool = False, force_download: bool = False, for_eda: bool = True
    ):
        """
        Convenience method to load, preprocess, and prepare data.

        Args:
            include_compas_score: Whether to include COMPAS scores
            force_download: Whether to force re-download
            for_eda: If True, return dict for EDA notebooks. If False, return tuple for modeling.

        Returns:
            If for_eda=True: Dict with keys 'data', 'metadata', 'sensitive_features'
            If for_eda=False: Tuple of (features, target)
        """
        if force_download:
            self.download()

        # Try to load processed data
        try:
            df = self.load_processed(f"compas_{self.task}")
            logger.info("Loaded preprocessed data from cache")
        except FileNotFoundError:
            # Process and save
            df_raw = self.load_raw()
            df = self.preprocess(df_raw)
            self.save_processed(df, f"compas_{self.task}")
            logger.info("Preprocessed and cached data")

        if for_eda:
            # Return format for EDA notebooks
            target_col = "two_year_recid" if self.task == "two_year" else "two_year_violent_recid"
            sensitive_cols = ["race", "sex", "age_cat"]

            # Extract components
            X, y, sensitive = self.get_X_y_sensitive(df)

            # Combine into single dataframe for EDA
            df_full = pd.concat([X, sensitive], axis=1)
            df_full[target_col] = y

            # Get metadata as dict
            metadata_obj = self.get_metadata()
            metadata_dict = {
                'name': metadata_obj.name,
                'task_type': metadata_obj.task_type,
                'n_samples': metadata_obj.n_samples,
                'n_features': metadata_obj.n_features,
                'n_classes': metadata_obj.n_classes,
                'target': target_col,
                'sensitive_features': metadata_obj.sensitive_features,
                'feature_names': metadata_obj.feature_names,
                'class_names': metadata_obj.class_names,
                'source': metadata_obj.source,
                'description': metadata_obj.description,
            }

            return {
                'data': df_full,
                'metadata': metadata_dict,
                'sensitive_features': sensitive
            }
        else:
            # Return tuple for modeling
            return self.prepare_for_modeling(df, include_compas_score)


# Backward compatibility alias for notebooks
COMPASDataLoader = COMPASLoader
