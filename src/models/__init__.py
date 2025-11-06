"""Model implementations for TabPFN criminology research."""

from .baselines import (
    LogisticRegressionModel,
    RandomForestModel,
    XGBoostModel,
    LightGBMModel,
    CatBoostModel,
    get_baseline_models,
)

__all__ = [
    "LogisticRegressionModel",
    "RandomForestModel",
    "XGBoostModel",
    "LightGBMModel",
    "CatBoostModel",
    "get_baseline_models",
]

# Optional TabPFN imports (require PyTorch)
try:
    from .tabpfn_model import TabPFNModel
    __all__.append("TabPFNModel")
except Exception:
    TabPFNModel = None

try:
    from .tabpfn_finetuner import TabPFNFinetuner
    __all__.append("TabPFNFinetuner")
except Exception:
    TabPFNFinetuner = None

try:
    from .localpfn import LocalPFN
    __all__.append("LocalPFN")
except Exception:
    LocalPFN = None
