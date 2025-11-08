# Archive Directory

**Purpose:** This directory contains files from the original automated pipeline that have been superseded by the new interactive notebook-based workflow.

**Date Archived:** 2025-11-08

---

## Why These Files Were Archived

This repository underwent a major transformation from an **automated script-based ML pipeline** to an **interactive, transparent, and ethically grounded analysis workflow** with 22 comprehensive Jupyter notebooks.

The files in this archive represent the **original automated approach** that has been replaced by the **new notebook-based approach**.

---

## What's In the Archive

### old_scripts/ (14 files)

**Automated Pipeline Scripts:**
- `make_all.sh` - Master shell orchestrator (ran entire pipeline in 12-48 hours)
- `run_experiment.py` - Core experiment runner
- `run_all_experiments.py` - Python orchestrator
- `demo_experiment.py` - Demo experiment runner

**Analysis Scripts (Superseded by Phase 4 Notebooks):**
- `analyze_calibration.py` → Replaced by notebooks in `notebooks/06_calibration_analysis/` (future)
- `analyze_calibration_from_predictions.py` → Replaced by calibration notebooks
- `analyze_fairness.py` → Replaced by `notebooks/05_fairness_analysis/05a_group_metrics.ipynb`
- `analyze_fairness_basic.py` → Replaced by fairness notebooks (05a-05d)

**Figure Generation Scripts (Superseded by Notebook Outputs):**
- `generate_figures.py` → Figures now generated inline in notebooks
- `generate_publication_figures.py` → Publication figures created in notebooks
- `populate_manuscript.py` → Tables/figures now in `results/` directory

**Utility Scripts:**
- `create_results_summary.py` → Results summarized in phase completion documents
- `run_bootstrap_ci.py` → Bootstrap analysis now in statistical utilities
- `fix_dependencies.py` → Dependencies now in requirements.txt/environment.yml

### old_documentation/ (9 files)

**Progress Logs (Historical):**
- `PHASE1_PROGRESS.md` - Superseded by `PHASE1_COMPLETE.md`
- `PHASE2_PROGRESS.md` - Superseded by `PHASE2_COMPLETE.md`
- `PROGRESS_SUMMARY.md` - Superseded by phase completion documents
- `EXPERIMENTAL_RESULTS.md` - Results now in `results/` directory

**Old Guides:**
- `EXPERIMENT_GUIDE.md` - Superseded by `USAGE_GUIDE.md`
- `DEMO_SUMMARY.md` - Demo content now in notebooks
- `RESULTS.md` - Results documented in phase summaries
- `TROUBLESHOOTING.md` - Troubleshooting now in `USAGE_GUIDE.md`

**Historical Planning:**
- `WORKPLAN_RESTRUCTURING.md` - **IMPORTANT HISTORICAL REFERENCE**
  - Documents the complete transformation plan
  - Shows original vision for 4-week restructuring
  - Outlines all phases (1-8) including future work
  - Valuable for understanding repository evolution

---

## Key Differences: Old vs New

| Aspect | Old Pipeline (Archived) | New Workflow (Active) |
|--------|-------------------------|----------------------|
| **Execution** | Automated scripts | Interactive notebooks |
| **Transparency** | Black-box execution | Step-by-step narrative |
| **Reproducibility** | Run entire pipeline | Run notebooks sequentially |
| **Documentation** | Separate from code | Integrated in notebooks |
| **Ethical Framework** | Not emphasized | Central to workflow |
| **Statistical Rigor** | Basic metrics | Pre-registered, corrected tests |
| **Fairness Analysis** | Single script | 4 comprehensive notebooks |
| **Publication Readiness** | Post-processing | Built-in throughout |

---

## What Was Retained from the Old Pipeline

While the scripts were archived, several components were **retained and improved**:

### Retained (in src/)
- ✅ **Data loading utilities** (`src/data_loader/`) - Enhanced
- ✅ **Model implementations** (`src/models/`) - Refactored
- ✅ **Evaluation metrics** (`src/evaluation/`) - Expanded
- ✅ **Statistical tests** - **NEW:** `src/statistics/` module added

### Not Retained
- ❌ Script orchestration (`make_all.sh`, `run_all_experiments.py`)
- ❌ Post-hoc analysis scripts (`analyze_*.py`)
- ❌ Figure generation scripts (`generate_*.py`)
- ❌ Progress logs (superseded by phase completion docs)

---

## Should You Use These Archived Files?

**No, unless:**
- You want to understand the original automated pipeline
- You're researching the repository's evolution
- You need to reproduce old experiments (not recommended)

**Instead, use:**
- `USAGE_GUIDE.md` - Comprehensive instructions for new workflow
- `notebooks/` - Interactive analysis workflow (22 notebooks)
- `PHASE[1-4]_COMPLETE.md` - Phase summaries
- `README.md` - Main repository documentation

---

## How the Transformation Happened

**Original State (Before Transformation):**
```
TabPFN-for-Criminology/
├── scripts/               # 12 Python scripts
│   ├── run_all_experiments.py
│   ├── analyze_*.py
│   └── generate_*.py
├── repro/
│   └── make_all.sh        # Master orchestrator
├── experiments/
│   └── run_experiment.py  # Core runner
└── src/                   # Utility modules
```

**After Transformation (Current):**
```
TabPFN-for-Criminology/
├── notebooks/             # 22 Jupyter notebooks
│   ├── 01_data_exploration/     (4 notebooks)
│   ├── 02_preprocessing/        (4 notebooks)
│   ├── 03_baseline_models/      (4 notebooks)
│   ├── 04_tabpfn_experiments/   (6 notebooks)
│   └── 05_fairness_analysis/    (4 notebooks)
├── src/
│   ├── statistics/        # NEW: Statistical utilities
│   ├── data_loader/       # Enhanced
│   ├── models/            # Refactored
│   └── evaluation/        # Expanded
├── docs/
│   ├── methodology/       # NEW: Analysis plan
│   └── ethics/            # NEW: Ethical framework
├── USAGE_GUIDE.md         # NEW: Comprehensive guide
├── REPOSITORY_OVERVIEW.md # NEW: Executive summary
└── archive/               # Old scripts and docs
```

---

## Timeline of Transformation

**Phase 1 (Foundation):**
- Created statistical utilities (`src/statistics/`)
- Wrote analysis plan (500 lines)
- Developed ethical framework (800 lines)

**Phase 2 (Core Notebooks):**
- Replaced data scripts → 4 exploration notebooks
- Replaced preprocessing → 4 preprocessing notebooks
- Replaced baseline models → 4 model notebooks

**Phase 3 (TabPFN Experiments):**
- Replaced TabPFN scripts → 6 comprehensive notebooks
- Added critical evaluation (04f_limitations)

**Phase 4 (Fairness Analysis):**
- Replaced `analyze_fairness.py` → 4 fairness notebooks
- Added intersectionality analysis
- Added trade-off analysis

**Cleanup (This Archive):**
- Moved old scripts to `archive/old_scripts/`
- Moved old documentation to `archive/old_documentation/`
- Created comprehensive usage guide

---

## For Historical Reference

If you're interested in the **rationale for the transformation**, read:

📄 **archive/old_documentation/WORKPLAN_RESTRUCTURING.md** (720 lines)
- Complete 4-week transformation plan
- Original vision and motivations
- Detailed notebook specifications
- Future phases (5-8) not yet implemented

This document explains **why** the transformation was necessary for publication in criminology research methods journals.

---

## Questions About the Archive?

If you have questions about:
- **Why a file was archived**: Read this README
- **How to use the new workflow**: See `USAGE_GUIDE.md`
- **What the repository does now**: See `README.md` or `REPOSITORY_OVERVIEW.md`
- **Technical details**: See `PHASE[1-4]_COMPLETE.md`

**Do not rely on archived scripts for current work.**

---

## Archive Maintenance

**These files are preserved for:**
- Historical reference
- Understanding repository evolution
- Academic transparency

**They will NOT be:**
- Updated or maintained
- Tested with new dependencies
- Supported in issues/PRs

**Last working version:** Commit prior to 2025-11-08 transformation

---

**For current usage, please see:** `USAGE_GUIDE.md` in the repository root.
