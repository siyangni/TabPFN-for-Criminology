"""TabPFN model wrapper for zero-shot inference."""

from typing import Union, Optional
import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class TabPFNModel:
    """
    Wrapper for TabPFN zero-shot inference.

    Provides a scikit-learn compatible interface for TabPFN
    classification and regression tasks.
    """

    def __init__(
        self,
        task_type: str = "classification",
        n_ensemble: int = 16,
        random_state: int = 42,
    ):
        """
        Initialize TabPFN model.

        Args:
            task_type: "classification" or "regression"
            n_ensemble: Number of ensemble members
            random_state: Random seed
        """
        self.task_type = task_type
        self.n_ensemble = n_ensemble
        self.random_state = random_state
        self.model = None

        self._load_model()

    def _load_model(self) -> None:
        """Load the appropriate TabPFN model."""
        try:
            if self.task_type == "classification":
                from tabpfn import TabPFNClassifier

                self.model = TabPFNClassifier(
                    n_estimators=self.n_ensemble,
                    device="cuda" if self._has_cuda() else "cpu",
                    random_state=self.random_state,
                )
                logger.info("Loaded TabPFNClassifier")

            elif self.task_type == "regression":
                from tabpfn import TabPFNRegressor

                self.model = TabPFNRegressor(
                    n_estimators=self.n_ensemble,
                    device="cuda" if self._has_cuda() else "cpu",
                    random_state=self.random_state,
                )
                logger.info("Loaded TabPFNRegressor")

            else:
                raise ValueError(f"Invalid task_type: {self.task_type}")

        except ImportError as e:
            logger.error(f"Failed to import TabPFN: {e}")
            logger.warning(
                "TabPFN not installed. Install with: pip install tabpfn"
            )
            raise

    def _has_cuda(self) -> bool:
        """Check if CUDA is available."""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False

    def fit(
        self,
        X: Union[np.ndarray, pd.DataFrame],
        y: Union[np.ndarray, pd.Series],
    ) -> "TabPFNModel":
        """
        Fit TabPFN model.

        Note: TabPFN uses in-context learning, so this stores the
        training data for prediction rather than traditional training.

        Args:
            X: Training features
            y: Training targets

        Returns:
            Fitted model
        """
        X_array = X.values if isinstance(X, pd.DataFrame) else X
        y_array = y.values if isinstance(y, pd.Series) else y

        logger.info(f"Fitting TabPFN on {X_array.shape[0]} samples")

        # Check dataset size constraints
        if X_array.shape[0] > 10000:
            logger.warning(
                f"Dataset has {X_array.shape[0]} samples. "
                f"TabPFN is optimized for datasets <10k samples. "
                f"Consider using a subsample or LocalPFN for larger datasets."
            )

        if X_array.shape[1] > 100:
            logger.warning(
                f"Dataset has {X_array.shape[1]} features. "
                f"TabPFN is optimized for <100 features. "
                f"Consider feature selection."
            )

        try:
            self.model.fit(X_array, y_array)
            logger.info("TabPFN fitted successfully")
        except Exception as e:
            logger.error(f"Error fitting TabPFN: {e}")
            raise

        return self

    def predict(self, X: Union[np.ndarray, pd.DataFrame]) -> np.ndarray:
        """
        Predict using fitted TabPFN model.

        Args:
            X: Test features

        Returns:
            Predictions
        """
        if self.model is None:
            raise ValueError("Model not fitted")

        X_array = X.values if isinstance(X, pd.DataFrame) else X

        try:
            predictions = self.model.predict(X_array)
            return predictions
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            raise

    def predict_proba(self, X: Union[np.ndarray, pd.DataFrame]) -> np.ndarray:
        """
        Predict class probabilities (classification only).

        Args:
            X: Test features

        Returns:
            Class probabilities
        """
        if self.task_type != "classification":
            raise ValueError("predict_proba only available for classification")

        if self.model is None:
            raise ValueError("Model not fitted")

        X_array = X.values if isinstance(X, pd.DataFrame) else X

        try:
            probas = self.model.predict_proba(X_array)
            return probas
        except Exception as e:
            logger.error(f"Error during probability prediction: {e}")
            raise

    def get_params(self) -> dict:
        """Get model parameters."""
        return {
            "task_type": self.task_type,
            "n_ensemble": self.n_ensemble,
            "random_state": self.random_state,
        }
