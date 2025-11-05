"""NCVS (National Crime Victimization Survey) dataset loader."""

import requests
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Dict
import logging

from .base_loader import BaseDataLoader, DatasetMetadata

logger = logging.getLogger(__name__)


class NCVSLoader(BaseDataLoader):
    """Loader for NCVS victimization data from BJS API."""

    API_BASE = "https://api.ojp.gov/bjsdataset/v1/"
    ENDPOINTS = {
        "personal_victimization": "gcuy-rt5g",
        "personal_population": "r4j4-fdwx",
        "household_victimization": "gkck-euys",
        "household_population": "ya4e-n9zp",
    }

    def __init__(
        self,
        data_dir: Path,
        endpoint: str = "personal_victimization",
        years: Optional[list] = None,
        limit: int = 500000,
        random_state: int = 42,
        test_size: float = 0.2,
        val_size: float = 0.1,
    ):
        """
        Initialize NCVS loader.

        Args:
            data_dir: Directory for data storage
            endpoint: API endpoint to use
            years: List of years to fetch (None = all available)
            limit: Maximum records to fetch per query
            random_state: Random seed
            test_size: Test set proportion
            val_size: Validation set proportion
        """
        super().__init__(data_dir, random_state, test_size, val_size)
        self.endpoint = endpoint
        self.years = years or list(range(2010, 2024))
        self.limit = limit

        if endpoint not in self.ENDPOINTS:
            raise ValueError(f"Endpoint must be one of {list(self.ENDPOINTS.keys())}")

        self.raw_dir = self.data_dir / "raw" / "ncvs"
        self.raw_dir.mkdir(parents=True, exist_ok=True)

    def download(self) -> None:
        """Download NCVS data from BJS API."""
        resource_id = self.ENDPOINTS[self.endpoint]

        # Construct years query
        years_str = ", ".join([f'"{year}"' for year in self.years])
        query = f"?$where=year in ({years_str})&$limit={self.limit}"

        url = f"{self.API_BASE}{resource_id}.json{query}"

        logger.info(f"Downloading NCVS data from {url}")

        try:
            response = requests.get(url, timeout=60)
            response.raise_for_status()

            data = response.json()

            # Save raw JSON
            output_path = (
                self.raw_dir / f"{self.endpoint}_{'_'.join(map(str, self.years))}.json"
            )

            import json

            with open(output_path, "w") as f:
                json.dump(data, f)

            logger.info(f"Downloaded {len(data)} records to {output_path}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Error downloading NCVS data: {e}")
            logger.warning("Using placeholder data for demonstration")
            # For demo purposes, create a minimal placeholder
            self._create_placeholder()

    def _create_placeholder(self) -> None:
        """Create placeholder NCVS data for testing."""
        logger.warning("Creating placeholder NCVS data")

        # Minimal synthetic data for demonstration
        n_samples = 1000
        np.random.seed(self.random_state)

        data = {
            "year": np.random.choice(self.years, n_samples),
            "age": np.random.randint(18, 80, n_samples),
            "sex": np.random.choice(["Male", "Female"], n_samples),
            "race": np.random.choice(
                ["White", "Black", "Hispanic", "Asian", "Other"], n_samples
            ),
            "income": np.random.choice(["<25k", "25-50k", "50-75k", ">75k"], n_samples),
            "victimization": np.random.choice([0, 1], n_samples, p=[0.9, 0.1]),
        }

        df = pd.DataFrame(data)
        output_path = self.raw_dir / f"{self.endpoint}_placeholder.csv"
        df.to_csv(output_path, index=False)

        logger.info(f"Created placeholder data at {output_path}")

    def load_raw(self) -> pd.DataFrame:
        """Load raw NCVS data."""
        # Try JSON first
        json_files = list(self.raw_dir.glob(f"{self.endpoint}_*.json"))

        if json_files:
            import json

            with open(json_files[0], "r") as f:
                data = json.load(f)
            df = pd.DataFrame(data)
        else:
            # Try CSV placeholder
            csv_files = list(self.raw_dir.glob(f"{self.endpoint}_*.csv"))
            if csv_files:
                df = pd.read_csv(csv_files[0])
            else:
                logger.info("No raw data found, downloading...")
                self.download()
                return self.load_raw()

        logger.info(f"Loaded {len(df)} rows from NCVS data")
        return df

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """Preprocess NCVS data."""
        logger.info(f"Preprocessing {len(df)} rows")

        # Basic preprocessing
        # Remove duplicates
        df = df.drop_duplicates()

        # Handle missing values
        df = df.dropna(subset=["victimization"] if "victimization" in df.columns else [])

        # Convert categorical variables
        categorical_cols = df.select_dtypes(include=["object"]).columns
        for col in categorical_cols:
            df[col] = df[col].astype("category")

        logger.info(f"After preprocessing: {len(df)} rows")

        return df

    def get_metadata(self) -> DatasetMetadata:
        """Get NCVS dataset metadata."""
        return DatasetMetadata(
            name=f"NCVS ({self.endpoint})",
            task_type="classification",
            n_samples=1000,  # Placeholder
            n_features=5,  # Placeholder
            n_classes=2,
            target_name="victimization",
            sensitive_features=["race", "sex", "age"],
            feature_names=["year", "age", "sex", "race", "income"],
            class_names=["No Victimization", "Victimization"],
            source="Bureau of Justice Statistics NCVS API",
            license="Public Domain (US Government)",
            description="National Crime Victimization Survey data",
        )

    def load_and_prepare(
        self, force_download: bool = False
    ) -> tuple[pd.DataFrame, pd.Series]:
        """Load and prepare NCVS data."""
        if force_download:
            self.download()

        try:
            df = self.load_processed(f"ncvs_{self.endpoint}")
        except FileNotFoundError:
            df_raw = self.load_raw()
            df = self.preprocess(df_raw)
            self.save_processed(df, f"ncvs_{self.endpoint}")

        # Prepare for modeling
        target_col = "victimization" if "victimization" in df.columns else df.columns[-1]
        X = df.drop(columns=[target_col])
        y = df[target_col]

        # One-hot encode
        X_encoded = pd.get_dummies(X, drop_first=True)

        return X_encoded, y
