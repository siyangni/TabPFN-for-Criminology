"""Baseline model implementations with hyperparameter tuning."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Union
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
from sklearn.linear_model import LogisticRegression, ElasticNet
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from xgboost import XGBClassifier, XGBRegressor
from lightgbm import LGBMClassifier, LGBMRegressor
from catboost import CatBoostClassifier, CatBoostRegressor
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
import optuna
import logging

logger = logging.getLogger(__name__)


class BaselineModel(ABC):
    """Base class for baseline models."""

    def __init__(
        self,
        task_type: str = "classification",
        random_state: int = 42,
        n_trials: int = 50,
        cv_folds: int = 5,
    ):
        """
        Initialize baseline model.

        Args:
            task_type: "classification" or "regression"
            random_state: Random seed
            n_trials: Number of Optuna trials for hyperparameter tuning
            cv_folds: Number of cross-validation folds
        """
        self.task_type = task_type
        self.random_state = random_state
        self.n_trials = n_trials
        self.cv_folds = cv_folds
        self.model: Optional[BaseEstimator] = None
        self.best_params: Optional[Dict[str, Any]] = None
        self.scaler: Optional[StandardScaler] = None

    @abstractmethod
    def get_param_space(self, trial: optuna.Trial) -> Dict[str, Any]:
        """Define hyperparameter search space."""
        pass

    @abstractmethod
    def create_model(self, params: Dict[str, Any]) -> BaseEstimator:
        """Create model with given parameters."""
        pass

    def tune_hyperparameters(
        self, X: np.ndarray, y: np.ndarray, class_weight: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Tune hyperparameters using Optuna.

        Args:
            X: Features
            y: Target
            class_weight: Class weighting strategy

        Returns:
            Best hyperparameters
        """
        optuna.logging.set_verbosity(optuna.logging.WARNING)

        def objective(trial):
            params = self.get_param_space(trial)
            if class_weight and self.task_type == "classification":
                params["class_weight"] = class_weight

            model = self.create_model(params)

            # Cross-validation scoring
            scoring = (
                "neg_log_loss" if self.task_type == "classification" else "neg_mean_squared_error"
            )

            try:
                scores = cross_val_score(
                    model,
                    X,
                    y,
                    cv=self.cv_folds,
                    scoring=scoring,
                    n_jobs=-1,
                )
                return scores.mean()
            except Exception as e:
                logger.warning(f"Trial failed: {e}")
                return float("-inf")

        study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=self.random_state))
        study.optimize(objective, n_trials=self.n_trials, show_progress_bar=False)

        self.best_params = study.best_params
        logger.info(f"Best params: {self.best_params}")
        logger.info(f"Best score: {study.best_value:.4f}")

        return self.best_params

    def fit(
        self,
        X: Union[np.ndarray, pd.DataFrame],
        y: Union[np.ndarray, pd.Series],
        tune: bool = True,
        class_weight: Optional[str] = None,
        scale: bool = False,
    ) -> "BaselineModel":
        """
        Fit the model.

        Args:
            X: Features
            y: Target
            tune: Whether to tune hyperparameters
            class_weight: Class weighting strategy
            scale: Whether to standardize features

        Returns:
            Fitted model
        """
        X_array = X.values if isinstance(X, pd.DataFrame) else X
        y_array = y.values if isinstance(y, pd.Series) else y

        # Scale features if requested
        if scale:
            self.scaler = StandardScaler()
            X_array = self.scaler.fit_transform(X_array)

        # Tune hyperparameters if requested
        if tune:
            params = self.tune_hyperparameters(X_array, y_array, class_weight)
        else:
            params = {}

        if class_weight and self.task_type == "classification":
            params["class_weight"] = class_weight

        # Fit final model
        self.model = self.create_model(params)
        self.model.fit(X_array, y_array)

        return self

    def predict(self, X: Union[np.ndarray, pd.DataFrame]) -> np.ndarray:
        """Predict labels."""
        if self.model is None:
            raise ValueError("Model not fitted")

        X_array = X.values if isinstance(X, pd.DataFrame) else X

        if self.scaler is not None:
            X_array = self.scaler.transform(X_array)

        return self.model.predict(X_array)

    def predict_proba(self, X: Union[np.ndarray, pd.DataFrame]) -> np.ndarray:
        """Predict probabilities (classification only)."""
        if self.model is None:
            raise ValueError("Model not fitted")

        if self.task_type != "classification":
            raise ValueError("predict_proba only available for classification")

        X_array = X.values if isinstance(X, pd.DataFrame) else X

        if self.scaler is not None:
            X_array = self.scaler.transform(X_array)

        return self.model.predict_proba(X_array)


class LogisticRegressionModel(BaselineModel):
    """Logistic Regression with elastic net regularization."""

    def get_param_space(self, trial: optuna.Trial) -> Dict[str, Any]:
        return {
            "C": trial.suggest_float("C", 1e-4, 1e2, log=True),
            "l1_ratio": trial.suggest_float("l1_ratio", 0.0, 1.0),
            "max_iter": 1000,
        }

    def create_model(self, params: Dict[str, Any]) -> BaseEstimator:
        return LogisticRegression(
            penalty="elasticnet",
            solver="saga",
            random_state=self.random_state,
            **params,
        )


class RandomForestModel(BaselineModel):
    """Random Forest classifier/regressor."""

    def get_param_space(self, trial: optuna.Trial) -> Dict[str, Any]:
        return {
            "n_estimators": trial.suggest_int("n_estimators", 50, 500),
            "max_depth": trial.suggest_int("max_depth", 3, 20),
            "min_samples_split": trial.suggest_int("min_samples_split", 2, 20),
            "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 10),
            "max_features": trial.suggest_categorical("max_features", ["sqrt", "log2", None]),
        }

    def create_model(self, params: Dict[str, Any]) -> BaseEstimator:
        if self.task_type == "classification":
            return RandomForestClassifier(
                random_state=self.random_state, n_jobs=-1, **params
            )
        else:
            return RandomForestRegressor(
                random_state=self.random_state, n_jobs=-1, **params
            )


class XGBoostModel(BaselineModel):
    """XGBoost classifier/regressor."""

    def get_param_space(self, trial: optuna.Trial) -> Dict[str, Any]:
        return {
            "n_estimators": trial.suggest_int("n_estimators", 50, 500),
            "max_depth": trial.suggest_int("max_depth", 3, 12),
            "learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.3, log=True),
            "subsample": trial.suggest_float("subsample", 0.6, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
            "min_child_weight": trial.suggest_int("min_child_weight", 1, 10),
            "reg_alpha": trial.suggest_float("reg_alpha", 1e-8, 1.0, log=True),
            "reg_lambda": trial.suggest_float("reg_lambda", 1e-8, 1.0, log=True),
        }

    def create_model(self, params: Dict[str, Any]) -> BaseEstimator:
        common_params = {
            "random_state": self.random_state,
            "n_jobs": -1,
            "tree_method": "hist",
            "early_stopping_rounds": 10,
        }

        if self.task_type == "classification":
            return XGBClassifier(**common_params, **params)
        else:
            return XGBRegressor(**common_params, **params)


class LightGBMModel(BaselineModel):
    """LightGBM classifier/regressor."""

    def get_param_space(self, trial: optuna.Trial) -> Dict[str, Any]:
        return {
            "n_estimators": trial.suggest_int("n_estimators", 50, 500),
            "max_depth": trial.suggest_int("max_depth", 3, 12),
            "learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.3, log=True),
            "num_leaves": trial.suggest_int("num_leaves", 20, 300),
            "subsample": trial.suggest_float("subsample", 0.6, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
            "min_child_samples": trial.suggest_int("min_child_samples", 5, 100),
            "reg_alpha": trial.suggest_float("reg_alpha", 1e-8, 1.0, log=True),
            "reg_lambda": trial.suggest_float("reg_lambda", 1e-8, 1.0, log=True),
        }

    def create_model(self, params: Dict[str, Any]) -> BaseEstimator:
        common_params = {
            "random_state": self.random_state,
            "n_jobs": -1,
            "verbosity": -1,
        }

        if self.task_type == "classification":
            return LGBMClassifier(**common_params, **params)
        else:
            return LGBMRegressor(**common_params, **params)


class CatBoostModel(BaselineModel):
    """CatBoost classifier/regressor."""

    def get_param_space(self, trial: optuna.Trial) -> Dict[str, Any]:
        return {
            "iterations": trial.suggest_int("iterations", 50, 500),
            "depth": trial.suggest_int("depth", 3, 10),
            "learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.3, log=True),
            "l2_leaf_reg": trial.suggest_float("l2_leaf_reg", 1e-8, 10.0, log=True),
            "subsample": trial.suggest_float("subsample", 0.6, 1.0),
        }

    def create_model(self, params: Dict[str, Any]) -> BaseEstimator:
        common_params = {
            "random_state": self.random_state,
            "verbose": 0,
            "allow_writing_files": False,
        }

        if self.task_type == "classification":
            return CatBoostClassifier(**common_params, **params)
        else:
            return CatBoostRegressor(**common_params, **params)


def get_baseline_models(
    task_type: str = "classification",
    random_state: int = 42,
    n_trials: int = 50,
    cv_folds: int = 5,
) -> Dict[str, BaselineModel]:
    """
    Get dictionary of all baseline models.

    Args:
        task_type: "classification" or "regression"
        random_state: Random seed
        n_trials: Number of Optuna trials
        cv_folds: Number of CV folds

    Returns:
        Dictionary mapping model names to model instances
    """
    models = {
        "logistic": LogisticRegressionModel(task_type, random_state, n_trials, cv_folds),
        "random_forest": RandomForestModel(task_type, random_state, n_trials, cv_folds),
        "xgboost": XGBoostModel(task_type, random_state, n_trials, cv_folds),
        "lightgbm": LightGBMModel(task_type, random_state, n_trials, cv_folds),
        "catboost": CatBoostModel(task_type, random_state, n_trials, cv_folds),
    }

    return models
