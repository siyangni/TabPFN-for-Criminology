#!/bin/bash

# Shell script to fix R dependency issues with curl and tidyverse
# This script provides multiple strategies to resolve the curl compilation error

set -e

echo "================================================================="
echo "R Dependency Fix Script (Bash version)"
echo "================================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if R is installed
if ! command -v R &> /dev/null; then
    echo -e "${RED}[ERROR] R is not installed or not in PATH${NC}"
    exit 1
fi

echo "[INFO] R version:"
R --version | head -n 1
echo ""

# Check system libcurl version
echo "[INFO] Checking system libcurl version..."
if command -v curl &> /dev/null; then
    curl --version | head -n 1
else
    echo -e "${YELLOW}[WARNING] curl command not found${NC}"
fi

# Check for libcurl development files
echo ""
echo "[INFO] Checking for libcurl development files..."
if pkg-config --exists libcurl; then
    echo "  libcurl version: $(pkg-config --modversion libcurl)"
    echo "  libcurl cflags: $(pkg-config --cflags libcurl)"
    echo "  libcurl libs: $(pkg-config --libs libcurl)"
else
    echo -e "${YELLOW}[WARNING] libcurl development files not found via pkg-config${NC}"
    echo "  This may cause issues when compiling R packages from source"
fi
echo ""

# Strategy 1: Use the R script
echo "================================================================="
echo "[STRATEGY 1] Running R dependency fix script..."
echo "================================================================="
echo ""

if [ -f "scripts/fix_r_dependencies.R" ]; then
    Rscript scripts/fix_r_dependencies.R
    exit_code=$?

    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}[SUCCESS] R dependencies fixed successfully!${NC}"
        exit 0
    else
        echo -e "${YELLOW}[WARNING] R script completed with errors${NC}"
    fi
else
    echo -e "${RED}[ERROR] fix_r_dependencies.R not found${NC}"
fi

# Strategy 2: Try using Conda/Mamba if available
echo ""
echo "================================================================="
echo "[STRATEGY 2] Checking for Conda/Mamba environment..."
echo "================================================================="
echo ""

if command -v conda &> /dev/null || command -v mamba &> /dev/null; then
    echo "[INFO] Conda/Mamba detected. You can create an R environment with:"
    echo ""
    echo "  conda create -n r-env r-base r-tidyverse r-here r-janitor r-skimr"
    echo "  conda activate r-env"
    echo ""
    echo "This will provide pre-compiled R packages that avoid compilation issues."
else
    echo "[INFO] Conda/Mamba not detected"
fi

# Strategy 3: Provide manual installation instructions
echo ""
echo "================================================================="
echo "[MANUAL INSTALLATION] Alternative approaches"
echo "================================================================="
echo ""
echo "If automatic installation failed, try these manual steps:"
echo ""
echo "1. Install specific older curl version (compatible with old libcurl):"
echo ""
echo "   R -e \"install.packages('https://cran.r-project.org/src/contrib/Archive/curl/curl_4.3.2.tar.gz', repos=NULL, type='source')\""
echo ""
echo "2. Install packages using binary builds (no compilation):"
echo ""
echo "   R -e \"install.packages('tidyverse', type='binary', repos='https://cran.rstudio.com/')\""
echo ""
echo "3. Update system libcurl (requires sudo/admin privileges):"
echo ""
echo "   # On Red Hat/CentOS/Rocky Linux:"
echo "   sudo yum install libcurl-devel"
echo ""
echo "   # On Debian/Ubuntu:"
echo "   sudo apt-get install libcurl4-openssl-dev"
echo ""
echo "4. Use renv for package management:"
echo ""
echo "   R -e \"install.packages('renv')\""
echo "   R -e \"renv::init()\""
echo "   R -e \"renv::install('tidyverse')\""
echo ""
echo "5. Contact your system administrator to:"
echo "   - Update libcurl to version 7.80.0 or higher"
echo "   - Install pre-compiled R packages system-wide"
echo ""

# Check if we're on a cluster/HPC system
if [ -f "/etc/redhat-release" ]; then
    echo "[INFO] Detected Red Hat-based system"
    cat /etc/redhat-release
    echo ""
    echo "Note: On HPC clusters, you may need to load modules:"
    echo "  module load curl"
    echo "  module load R"
fi

echo "================================================================="
echo "For more help, see TROUBLESHOOTING.md"
echo "================================================================="
