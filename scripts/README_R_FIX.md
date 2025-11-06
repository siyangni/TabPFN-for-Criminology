# R Dependency Fix Scripts

This directory contains scripts to fix common R package dependency issues, particularly with the `curl` package and `tidyverse`.

## Problem

When installing R packages that depend on `curl`, you may encounter this error:

```
unable to load shared object 'curl.so':
  undefined symbol: curl_url_strerror
ERROR: dependency 'curl' is not available for package 'tidyverse'
```

This occurs when:
- The R `curl` package is compiled against a newer libcurl API
- Your system has an older version of libcurl (< 7.80.0)
- The compiled package expects symbols that don't exist in your system's libcurl

## Quick Fix

### Option 1: Run the automated fix script (Recommended)

```bash
# Using the shell script
bash scripts/fix_r_dependencies.sh

# Or using the R script directly
Rscript scripts/fix_r_dependencies.R
```

### Option 2: Install older compatible version manually

```bash
# Install curl 4.3.2 (compatible with older libcurl)
R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/curl/curl_4.3.2.tar.gz', repos=NULL, type='source')"

# Then install tidyverse
R -e "install.packages('tidyverse')"
```

### Option 3: Use Conda (Best for HPC environments)

```bash
# Create R environment with pre-compiled packages
conda create -n r-env r-base r-tidyverse r-here r-janitor r-skimr -y
conda activate r-env

# Verify
R -e "library(tidyverse)"
```

## How the Fix Scripts Work

### `fix_r_dependencies.R`

This R script tries multiple strategies:

1. **Binary installation**: Attempts to install pre-compiled packages (fastest, no compilation)
2. **Older version**: Falls back to curl 4.3.2, which is compatible with older libcurl
3. **Custom configure**: Uses explicit library paths and configuration flags
4. **Verification**: Tests all installed packages

### `fix_r_dependencies.sh`

This bash script:

1. Checks your R and libcurl versions
2. Runs the R fix script
3. Provides manual alternatives if automated fix fails
4. Gives system-specific advice (Conda, HPC modules, etc.)

## What Gets Installed

The scripts install these R packages:

### Core packages:
- `curl`: HTTP client for R
- `httr`: Tools for working with URLs and HTTP
- `readr`: Fast reading of rectangular data (CSV, TSV)
- `dplyr`: Data manipulation
- `tidyr`: Data tidying
- `ggplot2`: Graphics
- `purrr`: Functional programming
- `tibble`: Modern data frames
- `stringr`: String operations
- `forcats`: Factor handling
- `lubridate`: Date/time handling

### Helper packages:
- `tidyverse`: Meta-package that loads all core packages
- `here`: Project-relative paths
- `janitor`: Data cleaning
- `skimr`: Data summaries

## Troubleshooting

### Still getting curl errors?

1. **Check your libcurl version:**
   ```bash
   curl --version
   pkg-config --modversion libcurl
   ```

2. **Check for development files:**
   ```bash
   pkg-config --exists libcurl && echo "OK" || echo "MISSING"
   ```

3. **On HPC systems, load modules:**
   ```bash
   module load curl/7.80.0  # or newer
   module load R
   ```

4. **Install libcurl dev files (requires admin):**
   ```bash
   # Red Hat/CentOS/Rocky
   sudo yum install libcurl-devel

   # Debian/Ubuntu
   sudo apt-get install libcurl4-openssl-dev
   ```

### Package installation fails with "404 Not Found"?

The archived curl version (4.3.2) may have moved. Try:

```bash
# List available archived versions
curl -s https://cran.r-project.org/src/contrib/Archive/curl/ | grep "curl_"

# Install a different compatible version (e.g., 4.3.3)
R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/curl/curl_4.3.3.tar.gz', repos=NULL, type='source')"
```

### Binary packages not available for your platform?

Some platforms (especially older systems) may not have binary packages. In this case:

1. Use Conda (recommended)
2. Update your system's libcurl
3. Contact your system administrator

## Testing the Fix

After running the fix, verify everything works:

```bash
R -e "
# Test imports
library(curl)
library(tidyverse)
library(here)
library(janitor)
library(skimr)

# Test functionality
df <- tibble::tibble(x = 1:5, y = letters[1:5])
print(df)

print('✓ All packages working correctly!')
"
```

## Environment-Specific Notes

### HPC Clusters

If you're on an HPC system, you likely don't have admin privileges. Use:

1. **Module system:**
   ```bash
   module spider curl
   module load curl/7.80.0  # or newer
   ```

2. **Conda:**
   ```bash
   conda create -n r-env r-base r-tidyverse
   conda activate r-env
   ```

3. **User installation:**
   ```bash
   R -e "install.packages('tidyverse', lib='~/R/library')"
   ```

### Docker

If you need a reproducible R environment:

```dockerfile
FROM rocker/tidyverse:latest

RUN install2.r --error \
    here \
    janitor \
    skimr

WORKDIR /workspace
```

### Singularity (for HPC)

```bash
# Pull a container with R and tidyverse
singularity pull docker://rocker/tidyverse:latest

# Run R in the container
singularity exec tidyverse_latest.sif R
```

## Why This Happens

The issue occurs because:

1. **R packages compile C code:** Many R packages (like `curl`) contain C code that must be compiled
2. **System library mismatch:** The C code links against your system's libcurl library
3. **ABI compatibility:** Newer R packages expect newer libcurl features
4. **Symbol resolution:** At runtime, the package looks for symbols (functions) in libcurl
5. **Missing symbols:** If libcurl is too old, the symbols don't exist → crash

The fix works by either:
- Using pre-compiled binaries (no compilation needed)
- Using older package versions (compatible with old libcurl)
- Updating the system library (adds missing symbols)

## Further Reading

- [R curl package documentation](https://cran.r-project.org/web/packages/curl/index.html)
- [Tidyverse installation guide](https://www.tidyverse.org/blog/2023/03/installing-r-packages/)
- [CRAN Binary Packages](https://cran.r-project.org/bin/)
- [Conda R Packages](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/use-r-with-conda.html)

## Support

For more help, see:
- `TROUBLESHOOTING.md` - Full troubleshooting guide
- [Open an issue](https://github.com/yourusername/TabPFN-for-Criminology/issues) - Report bugs
