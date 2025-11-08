# Notebook Import Fixes Required

**Issue Identified:** 2025-11-08
**Status:** Import errors in Phase 2 notebooks

---

## Problem Summary

The notebooks created during the transformation have import mismatches with the existing data loader module:

### Issue 1: Class Name Mismatch
- **Notebooks import:** `from data.compas_loader import COMPASDataLoader`
- **Actual class name:** `COMPASLoader` (in `src/data/compas_loader.py`)

### Issue 2: API Mismatch
- **Notebooks expect:** `loader.load_and_prepare()` to return a dictionary with keys:
  - `'data'` - DataFrame with features and target
  - `'metadata'` - Dataset metadata
  - `'sensitive_features'` - Sensitive attributes (race, sex, age_cat)

- **Actual return:** `load_and_prepare()` returns tuple `(X_encoded, y)`
  - `X_encoded` - One-hot encoded features (without sensitive attributes)
  - `y` - Target variable

---

## Affected Notebooks

Based on grep search, at least **2 notebooks** are affected:
1. `notebooks/01_data_exploration/01a_compas_eda.ipynb`
2. `notebooks/02_preprocessing/02a_data_cleaning.ipynb`

**Potentially more** - all Phase 2 notebooks may have this issue.

---

## Solution Options

### Option 1: Fix the Notebooks (Recommended)
Update notebooks to use the correct loader API:

```python
# Change from:
from data.compas_loader import COMPASDataLoader
loader = COMPASDataLoader(data_dir=DATA_DIR / "raw" / "compas")
data_dict = loader.load_and_prepare()
df = data_dict['data']
metadata = data_dict['metadata']
sensitive_attrs = data_dict['sensitive_features']

# To:
from data.compas_loader import COMPASLoader
from pathlib import Path

loader = COMPASLoader(data_dir=Path("data"))

# Load raw data and preprocess
df_raw = loader.load_raw()
df_processed = loader.preprocess(df_raw)

# Get features, target, and sensitive attributes separately
X, y, sensitive_attrs = loader.get_X_y_sensitive(df_processed)

# Combine for EDA (features + target + sensitive)
df_full = pd.concat([X, sensitive_attrs], axis=1)
df_full[target_col] = y

# Get metadata
metadata = loader.get_metadata()
```

### Option 2: Add Compatibility Layer
Add an alias and wrapper method to `src/data/__init__.py`:

```python
# In src/data/__init__.py, add:
COMPASDataLoader = COMPASLoader  # Alias for backward compatibility
```

And add a method to `COMPASLoader`:
```python
def load_data_for_eda(self):
    """Load data in format expected by EDA notebooks."""
    df_raw = self.load_raw()
    df_processed = self.preprocess(df_raw)
    X, y, sensitive = self.get_X_y_sensitive(df_processed)

    # Combine into single dataframe for EDA
    df_full = pd.concat([X, sensitive], axis=1)
    df_full[self.task + '_recid'] = y

    return {
        'data': df_full,
        'metadata': self.get_metadata().__dict__,
        'sensitive_features': sensitive
    }
```

### Option 3: Rewrite Data Loader (Not Recommended)
Modify the existing `COMPASLoader` to match notebook expectations.
**Risk:** May break other code that depends on current API.

---

## Recommended Fix

**Use Option 1** - Fix the notebooks to use the existing loader correctly.

**Rationale:**
- Preserves the existing, well-designed loader API
- Notebooks should adapt to utilities, not vice versa
- More maintainable long-term
- Only 2-22 notebooks need updating (vs changing core utilities)

---

## Implementation Plan

1. **Audit all notebooks** - Find all instances of `COMPASDataLoader` and `load_and_prepare()`
2. **Create template** - Standard data loading pattern for notebooks
3. **Systematic fix** - Update all affected notebooks
4. **Test** - Run first notebook to verify fix works
5. **Document** - Update USAGE_GUIDE.md with correct data loading pattern

---

## Next Steps

User should decide:
1. Fix notebooks systematically (recommended)
2. Add compatibility layer (quick fix)
3. Hybrid approach (both)

**Estimated time to fix:**
- All 22 notebooks: ~30-45 minutes
- Create compatibility layer: ~10 minutes
- Test and verify: ~15 minutes

---

**This document tracks the import mismatch issue and solution approaches.**
