# Correct Import Patterns for Notebooks

**Created:** 2025-11-08
**Purpose:** Reference guide for correct imports to avoid name collisions

---

## Common Import Issues

### Issue 1: Statistics Module Name Collision

Python has a built-in `statistics` module, which conflicts with our custom `src/statistics/` module.

❌ **WRONG:**
```python
from statistics import cohens_d, cohens_h, cramers_v
```
This imports from Python's built-in `statistics` module, which doesn't have these functions.

✅ **CORRECT:**
```python
from statistics.effect_sizes import cohens_d, cohens_h, cramers_v
```

---

## Complete Import Template for Notebooks

Use this template at the start of each notebook:

```python
# Standard library
import sys
from pathlib import Path
import json
from datetime import datetime

# Add src to path
project_root = Path.cwd().parent.parent
sys.path.insert(0, str(project_root / "src"))

# Data manipulation
import numpy as np
import pandas as pd

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Statistical tests (from scipy, not our module)
from scipy import stats

# Our modules - Data loading
from data import COMPASDataLoader

# Our modules - Statistical utilities
from statistics.effect_sizes import cohens_d, cohens_h, cramers_v
from statistics.hypothesis_tests import mcnemar_test, delong_test, permutation_test
from statistics.multiple_comparisons import holm_correction, benjamini_hochberg

# Configuration
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('colorblind')
pd.set_option('display.max_columns', None)
pd.set_option('display.precision', 3)

# Random seed for reproducibility
np.random.seed(42)

print("✓ Libraries imported successfully")
print(f"✓ Project root: {project_root}")
```

---

## Import Reference by Module

### Data Loading

```python
# COMPASLoader with alias
from data import COMPASDataLoader

# Direct import (also works)
from data.compas_loader import COMPASLoader

# Other loaders
from data import CommunitiesCrimeLoader, NCVSLoader, FBIUCRLoader
```

### Statistical Utilities

```python
# Effect sizes
from statistics.effect_sizes import (
    cohens_d,           # Standardized mean difference
    cohens_h,           # Effect size for proportions
    cramers_v,          # Association for categorical variables
    number_needed_to_evaluate  # NNE for predictions
)

# Hypothesis tests
from statistics.hypothesis_tests import (
    mcnemar_test,       # Paired predictions comparison
    delong_test,        # Correlated AUROC comparison
    permutation_test    # Non-parametric test
)

# Multiple comparisons
from statistics.multiple_comparisons import (
    holm_correction,           # FWER control (step-down)
    benjamini_hochberg,        # FDR control
    bonferroni_correction      # Conservative FWER
)
```

### External Statistical Functions

```python
# Use scipy.stats for standard tests
from scipy import stats

# Examples:
stats.chi2_contingency(...)   # Chi-squared test
stats.ttest_ind(...)          # Independent t-test
stats.mannwhitneyu(...)       # Mann-Whitney U test
```

---

## Troubleshooting Import Errors

### Error: "cannot import name 'cohens_d' from 'statistics'"

**Cause:** Importing from built-in `statistics` instead of `src/statistics/`

**Fix:**
```python
# Change from:
from statistics import cohens_d

# To:
from statistics.effect_sizes import cohens_d
```

---

### Error: "cannot import name 'COMPASDataLoader' from 'data.compas_loader'"

**Cause:** Missing kernel restart after adding alias

**Fix:**
1. Restart Jupyter kernel: `Kernel` → `Restart Kernel`
2. Or change import:
```python
# Change from:
from data.compas_loader import COMPASDataLoader

# To:
from data import COMPASDataLoader
```

---

### Error: "No module named 'data'"

**Cause:** `src/` directory not in Python path

**Fix:**
```python
# Add these lines at the top of notebook
import sys
from pathlib import Path

project_root = Path.cwd().parent.parent
sys.path.insert(0, str(project_root / "src"))
```

---

## Import Best Practices

### 1. Always Use Specific Imports

✅ **Good:**
```python
from statistics.effect_sizes import cohens_d, cohens_h
```

❌ **Avoid:**
```python
from statistics.effect_sizes import *
```

### 2. Import Order

Follow PEP 8 import order:
1. Standard library imports
2. Related third-party imports
3. Local application/library imports

### 3. Avoid Name Collisions

Be aware of built-in modules:
- `statistics` (built-in) vs `src/statistics/` (ours)
- `data` (potential namespace) vs `src/data/` (ours)
- `models` (potential conflict) vs `src/models/` (ours)

**Solution:** Always import from full module path when there might be conflicts.

---

## Quick Reference Table

| What You Need | Correct Import |
|--------------|----------------|
| COMPAS data loader | `from data import COMPASDataLoader` |
| Cohen's d | `from statistics.effect_sizes import cohens_d` |
| Cramér's V | `from statistics.effect_sizes import cramers_v` |
| DeLong test | `from statistics.hypothesis_tests import delong_test` |
| McNemar's test | `from statistics.hypothesis_tests import mcnemar_test` |
| Holm correction | `from statistics.multiple_comparisons import holm_correction` |
| Chi-squared test | `from scipy import stats` then `stats.chi2_contingency(...)` |

---

## Testing Your Imports

Run this cell to verify all imports work:

```python
# Test imports
try:
    from data import COMPASDataLoader
    print("✓ COMPASDataLoader imported")
except ImportError as e:
    print(f"✗ COMPASDataLoader failed: {e}")

try:
    from statistics.effect_sizes import cohens_d, cohens_h, cramers_v
    print("✓ Effect sizes imported")
except ImportError as e:
    print(f"✗ Effect sizes failed: {e}")

try:
    from statistics.hypothesis_tests import mcnemar_test, delong_test
    print("✓ Hypothesis tests imported")
except ImportError as e:
    print(f"✗ Hypothesis tests failed: {e}")

try:
    from statistics.multiple_comparisons import holm_correction
    print("✓ Multiple comparisons imported")
except ImportError as e:
    print(f"✗ Multiple comparisons failed: {e}")

print("\n✓ All imports successful!")
```

---

## For More Help

- See `USAGE_GUIDE.md` for complete notebook usage instructions
- See `NOTEBOOK_FIXES.md` for details on the backward compatibility layer
- Check `src/statistics/` for available statistical functions

---

**Remember:** When in doubt, use the full module path to avoid name collisions!
