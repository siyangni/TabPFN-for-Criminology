# Data Directory

This directory contains all datasets used in the TabPFN for Criminology research project.

## Directory Structure

### `raw/`
**Purpose:** Original, unmodified datasets as downloaded from sources.

**Contents:**
- `compas/` - ProPublica COMPAS recidivism data (Broward County, FL 2013-2014)
- `communities_crime/` - UCI Communities and Crime dataset
- `ncvs/` - National Crime Victimization Survey data (when available)
- `fbi_ucr/` - FBI Uniform Crime Reports data (when available)

**Guidelines:**
- Files in this directory should NEVER be modified
- Each subdirectory should contain:
  - Original data files
  - README with source URL and download date
  - Codebook or data dictionary (if available)
  - License information

### `interim/`
**Purpose:** Intermediate data files created during multi-step preprocessing.

**Contents:**
- Data files saved between preprocessing steps
- Useful for debugging and inspecting intermediate transformations
- Named with clear step indicators (e.g., `compas_step1_filtered.parquet`)

**Guidelines:**
- These files can be regenerated from raw data
- Document the transformation pipeline that creates each file
- Use parquet format for efficiency

### `processed/`
**Purpose:** Clean, analysis-ready datasets.

**Contents:**
- Final preprocessed datasets ready for modeling
- Train/test/validation splits
- Feature-engineered datasets
- Processing metadata and logs

**Guidelines:**
- All processed files should have accompanying metadata
- Use parquet format for typed, efficient storage
- Include checksums for verification
- Document all transformations applied

### `metadata/`
**Purpose:** Data dictionaries, codebooks, and dataset documentation.

**Contents:**
- Variable definitions and data dictionaries
- Codebooks from original sources
- Data provenance documentation
- Processing logs tracking all transformations
- Version information and checksums

## Data Formats

**Preferred formats:**
- `.parquet` - For processed tabular data (efficient, typed, compressed)
- `.csv` - For raw data and human-readable outputs
- `.json` - For metadata, logs, and configuration
- `.md` - For documentation

## Data Management Principles

1. **Immutability:** Raw data is never modified
2. **Reproducibility:** All processing steps are documented and scripted
3. **Transparency:** Clear lineage from raw to processed data
4. **Validation:** Data quality checks at each stage
5. **Privacy:** Sensitive data is never committed to git (see .gitignore)

## Gitignore Note

Data files are gitignored to avoid repository bloat. Only metadata and README files are version controlled. To reproduce the full dataset:

```bash
# Download raw data
python src/data/compas_loader.py --download

# Process data
jupyter notebook notebooks/02_preprocessing/02a_data_cleaning.ipynb
```

## Data Citation

When using data from this project, please cite:

**COMPAS:**
```
Angwin, J., Larson, J., Mattu, S., & Kirchner, L. (2016).
Machine Bias: Risk Assessments in Criminal Sentencing. ProPublica.
https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing
```

**Communities & Crime:**
```
Redmond, M. (2011). Communities and Crime Unnormalized Data Set.
UCI Machine Learning Repository.
https://archive.ics.uci.edu/ml/datasets/Communities+and+Crime+Unnormalized
```

For complete citations, see the manuscript bibliography.
