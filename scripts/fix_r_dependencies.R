#!/usr/bin/env Rscript
# Fix R dependencies for curl/tidyverse installation issues
# This script handles the common curl package compilation error

cat("=================================================================\n")
cat("R Dependency Fix Script\n")
cat("=================================================================\n\n")

# Function to install packages with better error handling
install_with_retry <- function(package, from_source = FALSE, version = NULL) {
  cat(sprintf("[INFO] Installing %s...\n", package))

  tryCatch({
    if (!is.null(version)) {
      # Install specific version
      pkg_string <- paste0(package, "_", version)
      cat(sprintf("  - Installing version %s\n", version))
      install.packages(pkg_string,
                      repos = "https://cran.rstudio.com/",
                      type = if(from_source) "source" else "binary",
                      dependencies = TRUE)
    } else {
      # Install latest version
      install.packages(package,
                      repos = "https://cran.rstudio.com/",
                      type = if(from_source) "source" else "binary",
                      dependencies = TRUE)
    }

    # Try to load the package
    library(package, character.only = TRUE)
    cat(sprintf("  ✓ Successfully installed and loaded %s\n\n", package))
    return(TRUE)
  }, error = function(e) {
    cat(sprintf("  ✗ Failed to install %s: %s\n\n", package, e$message))
    return(FALSE)
  })
}

# Check system curl version
cat("[INFO] Checking system libcurl version...\n")
system("curl --version | head -n 1")
cat("\n")

# Strategy 1: Try installing binary packages (pre-compiled)
cat("[STRATEGY 1] Attempting to install pre-compiled binary packages...\n")
cat("==============================================================\n\n")

# Try binary installation first (faster and avoids compilation issues)
binary_success <- install_with_retry("curl", from_source = FALSE)

if (!binary_success) {
  cat("[STRATEGY 2] Binary installation failed. Trying older compatible version...\n")
  cat("==============================================================\n\n")

  # Try older version of curl that's compatible with older libcurl
  # Version 4.3.2 is known to work with older libcurl versions
  cat("[INFO] Installing curl 4.3.2 (compatible with older libcurl)...\n")

  tryCatch({
    # Remove failed installation
    remove.packages("curl", lib = .libPaths()[1])
  }, error = function(e) {})

  # Install older version from source
  install.packages("https://cran.r-project.org/src/contrib/Archive/curl/curl_4.3.2.tar.gz",
                  repos = NULL,
                  type = "source")

  # Verify installation
  tryCatch({
    library(curl)
    cat("  ✓ Successfully installed curl 4.3.2\n\n")
    binary_success <- TRUE
  }, error = function(e) {
    cat("  ✗ Failed to install curl 4.3.2\n\n")
    binary_success <- FALSE
  })
}

if (!binary_success) {
  cat("[STRATEGY 3] Trying to configure curl package with system flags...\n")
  cat("==============================================================\n\n")

  # Set environment variables to help find system libraries
  Sys.setenv(CURL_INCLUDES = "/usr/include")
  Sys.setenv(CURL_LIBS = "-lcurl")

  # Try one more time with explicit library paths
  tryCatch({
    remove.packages("curl", lib = .libPaths()[1])
  }, error = function(e) {})

  install.packages("curl",
                  repos = "https://cran.rstudio.com/",
                  type = "source",
                  configure.args = "--with-curl=/usr")
}

# Now install the rest of the tidyverse dependencies
cat("\n[INFO] Installing tidyverse and dependencies...\n")
cat("==============================================================\n\n")

required_packages <- c("httr", "rvest", "readr", "dplyr", "tidyr",
                       "ggplot2", "purrr", "tibble", "stringr",
                       "forcats", "lubridate")

for (pkg in required_packages) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    install_with_retry(pkg, from_source = FALSE)
  } else {
    cat(sprintf("  ✓ %s already installed\n", pkg))
  }
}

# Finally install tidyverse meta-package
cat("\n[INFO] Installing tidyverse meta-package...\n")
install_with_retry("tidyverse", from_source = FALSE)

# Install other useful packages mentioned in the error
cat("\n[INFO] Installing additional helper packages...\n")
cat("==============================================================\n\n")

additional_packages <- c("here", "janitor", "skimr")
for (pkg in additional_packages) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    install_with_retry(pkg, from_source = FALSE)
  } else {
    cat(sprintf("  ✓ %s already installed\n", pkg))
  }
}

# Verification
cat("\n=================================================================\n")
cat("VERIFICATION\n")
cat("=================================================================\n\n")

verify_packages <- c("curl", "tidyverse", "readr", "here", "janitor", "skimr")
all_ok <- TRUE

for (pkg in verify_packages) {
  result <- tryCatch({
    library(pkg, character.only = TRUE)
    cat(sprintf("  ✓ %s: OK\n", pkg))
    TRUE
  }, error = function(e) {
    cat(sprintf("  ✗ %s: FAILED\n", pkg))
    all_ok <<- FALSE
    FALSE
  })
}

cat("\n")
if (all_ok) {
  cat("[SUCCESS] All packages installed successfully!\n")
  cat("\nYou can now use:\n")
  cat("  library(tidyverse)\n")
  cat("  read_tsv('file.tsv')\n")
  cat("\n")
  quit(status = 0)
} else {
  cat("[WARNING] Some packages failed to install.\n")
  cat("\nPossible solutions:\n")
  cat("1. Update your system's libcurl library (requires admin privileges)\n")
  cat("2. Use an older R version (3.6.x series has better compatibility)\n")
  cat("3. Use Docker/Conda environment with pre-configured R\n")
  cat("4. Contact your system administrator to update libcurl\n")
  cat("\n")
  quit(status = 1)
}
