# Troubleshooting Guide

## Issue 1: NumPy 2.x Compatibility Error

**Error message:**
```
A module that was compiled using NumPy 1.x cannot be run in
NumPy 2.1.3 as it may crash.
AttributeError: _ARRAY_API not found
```

**Cause:** You have NumPy 2.1.3 installed, but pandas/pyarrow were compiled against NumPy 1.x.

**Solution:** Downgrade NumPy to 1.x

```bash
pip install "numpy<2.0"
```

Or more specifically:

```bash
pip install "numpy==1.26.4"
```

## Issue 2: Missing ucimlrepo Module

**Error message:**
```
ModuleNotFoundError: No module named 'ucimlrepo'
```

**Solution:** Install the missing package

```bash
pip install ucimlrepo
```

## Quick Fix (All Issues)

Run these commands in order:

```bash
# 1. Downgrade NumPy
pip install "numpy<2.0"

# 2. Install missing packages
pip install ucimlrepo

# 3. Verify installations
python -c "import numpy; print(f'NumPy: {numpy.__version__}')"
python -c "import pandas; print(f'Pandas: {pandas.__version__}')"
python -c "import ucimlrepo; print('ucimlrepo: OK')"

# 4. Now run the demo
python scripts/demo_experiment.py
```

## Alternative: Create Clean Virtual Environment

If issues persist, create a fresh virtual environment:

```bash
# Create new environment
python -m venv venv_clean
source venv_clean/bin/activate  # On Windows: venv_clean\Scripts\activate

# Install requirements with compatible NumPy
pip install "numpy<2.0"
pip install pandas scikit-learn matplotlib seaborn
pip install xgboost lightgbm catboost optuna
pip install ucimlrepo requests tqdm pyyaml

# Run demo
python scripts/demo_experiment.py
```

## Using Conda (Recommended for Complex Dependencies)

```bash
# Create conda environment
conda create -n tabpfn-crim python=3.10 -y
conda activate tabpfn-crim

# Install packages
conda install numpy=1.26 pandas scikit-learn matplotlib seaborn -y
conda install -c conda-forge xgboost lightgbm optuna -y
pip install catboost ucimlrepo

# Run demo
python scripts/demo_experiment.py
```

## Environment File with Fixed Versions

Create a file `requirements_fixed.txt`:

```
numpy==1.26.4
pandas==2.1.4
scikit-learn==1.3.2
matplotlib==3.8.2
seaborn==0.13.0
scipy==1.11.4
xgboost==2.0.3
lightgbm==4.1.0
catboost==1.2.2
optuna==3.4.0
ucimlrepo==0.0.3
requests==2.31.0
tqdm==4.66.1
pyyaml==6.0.1
```

Then install:

```bash
pip install -r requirements_fixed.txt
```

## Checking Your Current Environment

```bash
# Check Python version
python --version

# Check NumPy version
python -c "import numpy; print(numpy.__version__)"

# Check all installed packages
pip list | grep -E "numpy|pandas|xgboost|ucimlrepo"

# Check if modules import correctly
python -c "
import sys
sys.path.insert(0, 'src')
from data import COMPASLoader
print('✓ COMPASLoader imports successfully')
"
```

## Common Issues on HPC Systems

If you're on an HPC system (like PSC), you may need to:

1. **Load required modules:**
```bash
module load python/3.10
module load gcc/11.2.0  # For compiling some packages
```

2. **Install in user directory:**
```bash
pip install --user "numpy<2.0" ucimlrepo
```

3. **Check for conflicting system packages:**
```bash
# See what's loaded
pip list

# If there are system-wide packages causing conflicts, create a virtual env:
python -m venv --system-site-packages venv
source venv/bin/activate
pip install --upgrade pip
pip install "numpy<2.0" ucimlrepo
```

## Verifying the Fix

After applying fixes, test with:

```bash
python -c "
import sys
sys.path.insert(0, 'src')

# Test imports
import numpy as np
import pandas as pd
from data import COMPASLoader
from models import LogisticRegressionModel

print(f'✓ NumPy {np.__version__}')
print(f'✓ Pandas {pd.__version__}')
print('✓ All imports successful!')
"
```

## Still Having Issues?

If problems persist:

1. **Check your Python path:**
```bash
which python
python -c "import sys; print(sys.executable)"
```

2. **Check for multiple Python installations:**
```bash
which -a python python3
```

3. **Clear pip cache:**
```bash
pip cache purge
```

4. **Reinstall problematic packages:**
```bash
pip uninstall numpy pandas pyarrow -y
pip install "numpy<2.0" "pandas<2.3" "pyarrow>=14.0"
```

## Contact & Support

If you continue to have issues, please open an issue on GitHub with:
- Your Python version (`python --version`)
- Your OS and environment (conda, venv, system Python)
- Full error traceback
- Output of `pip list`
