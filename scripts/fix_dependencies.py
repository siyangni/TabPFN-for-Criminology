"""Quick fix script for dependency issues."""

import subprocess
import sys

print("Fixing dependency issues...")
print("=" * 80)

# Fix 1: Downgrade NumPy to 1.x (compatible with pandas/pyarrow)
print("\n1. Downgrading NumPy to 1.26.4 (compatible with pandas/pyarrow)...")
subprocess.run([sys.executable, "-m", "pip", "install", "numpy<2.0"], check=True)

# Fix 2: Install missing ucimlrepo
print("\n2. Installing ucimlrepo...")
subprocess.run([sys.executable, "-m", "pip", "install", "ucimlrepo"], check=True)

# Fix 3: Ensure other key packages are compatible
print("\n3. Ensuring compatible versions of key packages...")
subprocess.run([sys.executable, "-m", "pip", "install", "pandas>=2.0,<2.3", "pyarrow>=14.0"], check=True)

print("\n" + "=" * 80)
print("✓ Dependencies fixed!")
print("\nYou can now run: python scripts/demo_experiment.py")
