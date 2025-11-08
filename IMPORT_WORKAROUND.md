# Import Workaround for Statistics Module Name Collision

**Issue:** Python's built-in `statistics` module conflicts with `src/statistics/`

**Severity:** CRITICAL - Blocks all notebooks

---

## The Problem

Python's standard library includes a `statistics` module, which takes priority over our custom `src/statistics/` module even when we add `src` to `sys.path`.

When you try:
```python
sys.path.insert(0, str(project_root / "src"))
from statistics.effect_sizes import cohens_d
```

Python finds the built-in `statistics` module first, which is NOT a package (just a single .py file), so it can't have submodules like `effect_sizes`.

---

## Quick Workaround (Use This Now)

Add this to your notebook BEFORE importing from statistics:

```python
# Standard library
import sys
from pathlib import Path

# Add src to path
project_root = Path.cwd().parent.parent
sys.path.insert(0, str(project_root / "src"))

# WORKAROUND: Remove built-in statistics module from cache
# This forces Python to use our custom statistics module
if 'statistics' in sys.modules:
    del sys.modules['statistics']

# NOW import from our statistics module (will work!)
from data import COMPASDataLoader
from statistics.effect_sizes import cohens_d, cohens_h, cramers_v
from statistics.hypothesis_tests import permutation_test
```

---

## Complete Working Import Block

```python
# Standard library
import sys
from pathlib import Path
import json
from datetime import datetime

# Add src to path
project_root = Path.cwd().parent.parent
sys.path.insert(0, str(project_root / "src"))

# CRITICAL: Remove built-in statistics from module cache
if 'statistics' in sys.modules:
    del sys.modules['statistics']

# Data manipulation
import numpy as np
import pandas as pd

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Statistical tests (use scipy for standard stats)
from scipy import stats

# Our modules
from data import COMPASDataLoader
from statistics.effect_sizes import cohens_d, cohens_h, cramers_v
from statistics.hypothesis_tests import permutation_test

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

## Why This Works

1. We add `src/` to `sys.path` first
2. We delete the built-in `statistics` module from `sys.modules` cache
3. When Python tries to import `from statistics.effect_sizes`, it:
   - Doesn't find `statistics` in the cache
   - Searches `sys.path` (which now has `src/` first)
   - Finds `src/statistics/` and loads our custom module

---

## Long-Term Solution (Recommended)

Rename `src/statistics/` to avoid the collision entirely.

**Option 1: Rename to `stats_utils`**
```bash
mv src/statistics src/stats_utils
# Update all imports to:
from stats_utils.effect_sizes import cohens_d
```

**Option 2: Rename to `statistical_tests`**
```bash
mv src/statistics src/statistical_tests
# Update all imports to:
from statistical_tests.effect_sizes import cohens_d
```

**Option 3: Rename to `custom_stats`**
```bash
mv src/statistics src/custom_stats
# Update all imports to:
from custom_stats.effect_sizes import cohens_d
```

**Effort:**
- Rename directory: 2 minutes
- Update all 22 notebooks: 30-45 minutes
- Update any other files that import from statistics: 10 minutes
- Total: ~1 hour

**Benefits:**
- Cleaner, no workarounds needed
- No risk of accidentally importing built-in module
- More maintainable long-term

---

## Recommendation

**For now:** Use the workaround above (delete from sys.modules)

**For production:** Rename the directory to `stats_utils` or similar

---

## Testing the Workaround

Run this to verify it works:

```python
import sys
from pathlib import Path

# Setup path
project_root = Path.cwd().parent.parent
sys.path.insert(0, str(project_root / "src"))

# Apply workaround
if 'statistics' in sys.modules:
    del sys.modules['statistics']

# Test imports
try:
    from statistics.effect_sizes import cohens_d
    print("✓ cohens_d imported successfully")
    print(f"  From: {cohens_d.__module__}")
except Exception as e:
    print(f"✗ Failed: {e}")

try:
    from statistics.hypothesis_tests import delong_test
    print("✓ delong_test imported successfully")
    print(f"  From: {delong_test.__module__}")
except Exception as e:
    print(f"✗ Failed: {e}")
```

Expected output:
```
✓ cohens_d imported successfully
  From: statistics.effect_sizes
✓ delong_test imported successfully
  From: statistics.hypothesis_tests
```

---

**This workaround should unblock all notebooks immediately!**
