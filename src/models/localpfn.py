"""LocalPFN: Retrieval-augmented TabPFN with fine-tuning."""

from typing import Union, Optional, Tuple
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import logging

from .tabpfn_finetuner import TabPFNFinetuner

logger = logging.getLogger(__name__)


class LocalPFN:
    """
    LocalPFN implementation combining retrieval and fine-tuning.

    This implements the approach from "Improving Tabular Foundation Models
    with Retrieval-Augmented In-Context Learning" (Yu et al., 2024).

    The key idea is to:
    1. Retrieve K nearest neighbors for each test instance
    2. Fine-tune TabPFN on the retrieved local context
    3. Make predictions using the locally-adapted model
    """

    def __init__(
        self,
        task_type: str = "classification",
        retrieval_k: int = 50,
        retrieval_metric: str = "euclidean",
        fine_tune: bool = True,
        learning_rate: float = 1e-5,
        batch_size: int = 20,
        max_epochs: int = 30,
        early_stop_patience: int = 3,
        random_state: int = 42,
    ):
        """
        Initialize LocalPFN.

        Args:
            task_type: "classification" or "regression"
            retrieval_k: Number of nearest neighbors to retrieve
            retrieval_metric: Distance metric for retrieval
            fine_tune: Whether to fine-tune on retrieved context
            learning_rate: Learning rate for fine-tuning
            batch_size: Batch size for fine-tuning
            max_epochs: Maximum epochs for fine-tuning
            early_stop_patience: Early stopping patience
            random_state: Random seed
        """
        self.task_type = task_type
        self.retrieval_k = retrieval_k
        self.retrieval_metric = retrieval_metric
        self.fine_tune = fine_tune
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.max_epochs = max_epochs
        self.early_stop_patience = early_stop_patience
        self.random_state = random_state

        self.retriever: Optional[NearestNeighbors] = None
        self.scaler: Optional[StandardScaler] = None
        self.X_train: Optional[np.ndarray] = None
        self.y_train: Optional[np.ndarray] = None
        self.finetuner: Optional[TabPFNFinetuner] = None

        logger.info(
            f"LocalPFN initialized with k={retrieval_k}, "
            f"fine_tune={fine_tune}, metric={retrieval_metric}"
        )

    def fit(
        self,
        X: Union[np.ndarray, pd.DataFrame],
        y: Union[np.ndarray, pd.Series],
    ) -> "LocalPFN":
        """
        Fit LocalPFN by building the retrieval index.

        Args:
            X: Training features
            y: Training targets

        Returns:
            Fitted LocalPFN
        """
        # Convert to numpy
        self.X_train = X.values if isinstance(X, pd.DataFrame) else X
        self.y_train = y.values if isinstance(y, pd.Series) else y

        logger.info(f"Fitting LocalPFN on {len(self.X_train)} samples")

        # Standardize features for retrieval
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(self.X_train)

        # Build retrieval index (KNN)
        self.retriever = NearestNeighbors(
            n_neighbors=min(self.retrieval_k, len(self.X_train)),
            metric=self.retrieval_metric,
            algorithm="auto",
            n_jobs=-1,
        )
        self.retriever.fit(X_scaled)

        logger.info("Retrieval index built successfully")

        return self

    def _retrieve_context(
        self, X_query: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Retrieve local context for query points.

        Args:
            X_query: Query points

        Returns:
            Tuple of (retrieved_X, retrieved_y)
        """
        if self.retriever is None:
            raise ValueError("Model not fitted")

        # Scale query points
        X_query_scaled = self.scaler.transform(X_query)

        # Retrieve neighbors
        distances, indices = self.retriever.kneighbors(X_query_scaled)

        # For batch queries, we need to aggregate retrieved contexts
        # Simple approach: union of all retrieved neighbors
        unique_indices = np.unique(indices.flatten())

        X_context = self.X_train[unique_indices]
        y_context = self.y_train[unique_indices]

        logger.info(
            f"Retrieved {len(X_context)} unique samples "
            f"for {len(X_query)} query points"
        )

        return X_context, y_context

    def predict(
        self, X: Union[np.ndarray, pd.DataFrame], return_context: bool = False
    ) -> Union[np.ndarray, Tuple[np.ndarray, int]]:
        """
        Predict using LocalPFN.

        For each test batch:
        1. Retrieve K nearest neighbors
        2. Fine-tune TabPFN on retrieved context (if fine_tune=True)
        3. Predict on test batch

        Args:
            X: Test features
            return_context: Whether to return context size used

        Returns:
            Predictions (and optionally context size)
        """
        X_array = X.values if isinstance(X, pd.DataFrame) else X

        # Retrieve local context
        X_context, y_context = self._retrieve_context(X_array)

        if self.fine_tune:
            # Fine-tune TabPFN on retrieved context
            logger.info("Fine-tuning on retrieved context")

            self.finetuner = TabPFNFinetuner(
                task_type=self.task_type,
                learning_rate=self.learning_rate,
                batch_size=self.batch_size,
                max_epochs=self.max_epochs,
                early_stop_patience=self.early_stop_patience,
                random_state=self.random_state,
            )

            # Split context into train/val for fine-tuning
            split_idx = int(0.8 * len(X_context))
            X_train_context = X_context[:split_idx]
            y_train_context = y_context[:split_idx]
            X_val_context = X_context[split_idx:]
            y_val_context = y_context[split_idx:]

            self.finetuner.fit(
                X_train_context, y_train_context, X_val_context, y_val_context
            )

            # Predict using fine-tuned model
            predictions = self.finetuner.predict(X_array)

        else:
            # Use zero-shot TabPFN on retrieved context
            from .tabpfn_model import TabPFNModel

            logger.info("Using zero-shot TabPFN on retrieved context")

            model = TabPFNModel(
                task_type=self.task_type, random_state=self.random_state
            )
            model.fit(X_context, y_context)
            predictions = model.predict(X_array)

        if return_context:
            return predictions, len(X_context)
        else:
            return predictions

    def predict_proba(
        self, X: Union[np.ndarray, pd.DataFrame]
    ) -> np.ndarray:
        """
        Predict probabilities (classification only).

        Args:
            X: Test features

        Returns:
            Class probabilities
        """
        if self.task_type != "classification":
            raise ValueError("predict_proba only available for classification")

        X_array = X.values if isinstance(X, pd.DataFrame) else X

        # Retrieve local context
        X_context, y_context = self._retrieve_context(X_array)

        if self.fine_tune:
            # Fine-tune TabPFN on retrieved context
            logger.info("Fine-tuning on retrieved context")

            self.finetuner = TabPFNFinetuner(
                task_type=self.task_type,
                learning_rate=self.learning_rate,
                batch_size=self.batch_size,
                max_epochs=self.max_epochs,
                early_stop_patience=self.early_stop_patience,
                random_state=self.random_state,
            )

            # Split context into train/val
            split_idx = int(0.8 * len(X_context))
            X_train_context = X_context[:split_idx]
            y_train_context = y_context[:split_idx]
            X_val_context = X_context[split_idx:]
            y_val_context = y_context[split_idx:]

            self.finetuner.fit(
                X_train_context, y_train_context, X_val_context, y_val_context
            )

            # Predict probabilities
            probas = self.finetuner.predict_proba(X_array)

        else:
            # Use zero-shot TabPFN
            from .tabpfn_model import TabPFNModel

            logger.info("Using zero-shot TabPFN on retrieved context")

            model = TabPFNModel(
                task_type=self.task_type, random_state=self.random_state
            )
            model.fit(X_context, y_context)
            probas = model.predict_proba(X_array)

        return probas

    def get_params(self) -> dict:
        """Get LocalPFN parameters."""
        return {
            "task_type": self.task_type,
            "retrieval_k": self.retrieval_k,
            "retrieval_metric": self.retrieval_metric,
            "fine_tune": self.fine_tune,
            "learning_rate": self.learning_rate,
        }
