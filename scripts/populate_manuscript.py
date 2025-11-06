"""
Populate manuscript with experimental results.

This script:
1. Loads experimental results from JSON files
2. Generates markdown tables for Results section
3. Auto-fills key findings in Discussion section
4. Creates comprehensive results summary
5. Updates manuscript_draft.md with actual numbers

Usage:
    python scripts/populate_manuscript.py --results experiments/results --manuscript paper/manuscript_draft.md
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import json
import argparse
import numpy as np
import pandas as pd
from typing import Dict, List
from datetime import datetime

from utils import setup_logger

logger = setup_logger("populate_manuscript")


def load_all_results(results_dir: Path) -> Dict:
    """Load all experimental results from directory structure."""

    all_results = {}

    for dataset_dir in results_dir.iterdir():
        if not dataset_dir.is_dir():
            continue

        dataset_name = dataset_dir.name
        all_results[dataset_name] = {}

        # Look for model result files
        for json_file in dataset_dir.glob("**/*.json"):
            if "config" in json_file.name or "versions" in json_file.name or "bootstrap" in json_file.name:
                continue

            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)

                # Extract model name
                model_name = json_file.stem
                if "model" in data:
                    model_name = data["model"]
                elif "model_name" in data:
                    model_name = data["model_name"]

                all_results[dataset_name][model_name] = data
                logger.info(f"Loaded {dataset_name}/{model_name}")

            except Exception as e:
                logger.warning(f"Could not load {json_file}: {e}")

    return all_results


def generate_performance_table(results: Dict, dataset: str) -> str:
    """Generate markdown table of performance metrics."""

    if dataset not in results or not results[dataset]:
        return "*No results available for this dataset.*"

    model_results = results[dataset]

    # Prepare table data
    rows = []
    for model_name, data in model_results.items():
        row = {"Model": model_name}

        if "metrics" in data:
            metrics = data["metrics"]
            row["AUROC"] = f"{metrics.get('auroc', np.nan):.3f}"
            row["AUPRC"] = f"{metrics.get('auprc', np.nan):.3f}"
            row["F1"] = f"{metrics.get('f1', np.nan):.3f}"
            row["Accuracy"] = f"{metrics.get('accuracy', np.nan):.3f}"

        if "calibration" in data:
            cal = data["calibration"]
            row["Brier"] = f"{cal.get('brier_score', np.nan):.3f}"
            row["ECE"] = f"{cal.get('ece', np.nan):.3f}"

        if "fairness" in data and "race" in data["fairness"]:
            fair = data["fairness"]["race"]
            row["EOD"] = f"{fair.get('equalized_odds_difference', np.nan):.3f}"

        rows.append(row)

    df = pd.DataFrame(rows)

    # Convert to markdown
    markdown = df.to_markdown(index=False)

    return markdown


def generate_key_findings(results: Dict) -> List[str]:
    """Generate key findings from results."""

    findings = []

    # Compare models across datasets
    for dataset, models in results.items():
        if not models:
            continue

        # Find best model by AUROC
        aurocs = {model: data["metrics"]["auroc"]
                 for model, data in models.items()
                 if "metrics" in data and "auroc" in data["metrics"]}

        if aurocs:
            best_model = max(aurocs, key=aurocs.get)
            best_auroc = aurocs[best_model]

            findings.append(
                f"On {dataset}, {best_model} achieved the highest AUROC ({best_auroc:.3f})"
            )

        # Check TabPFN vs baselines
        tabpfn_models = [m for m in models if "tabpfn" in m.lower()]
        baseline_models = [m for m in models if m.lower() in ["logistic", "xgboost", "lightgbm", "catboost"]]

        if tabpfn_models and baseline_models:
            tabpfn_auroc = np.mean([models[m]["metrics"]["auroc"]
                                   for m in tabpfn_models
                                   if "metrics" in models[m] and "auroc" in models[m]["metrics"]])

            baseline_auroc = np.mean([models[m]["metrics"]["auroc"]
                                     for m in baseline_models
                                     if "metrics" in models[m] and "auroc" in models[m]["metrics"]])

            if tabpfn_auroc > baseline_auroc:
                improvement = ((tabpfn_auroc - baseline_auroc) / baseline_auroc) * 100
                findings.append(
                    f"TabPFN variants improved AUROC by {improvement:.1f}% over baselines on {dataset}"
                )
            else:
                decline = ((baseline_auroc - tabpfn_auroc) / baseline_auroc) * 100
                findings.append(
                    f"Baselines outperformed TabPFN by {decline:.1f}% on {dataset} "
                    f"(possibly due to small dataset size)"
                )

        # Check calibration
        for model, data in models.items():
            if "calibration" in data and "ece" in data["calibration"]:
                ece = data["calibration"]["ece"]

                if ece < 0.05:
                    findings.append(f"{model} on {dataset} is well-calibrated (ECE={ece:.3f})")
                elif ece > 0.10:
                    findings.append(f"{model} on {dataset} shows poor calibration (ECE={ece:.3f})")

        # Check fairness
        for model, data in models.items():
            if "fairness" in data and "race" in data["fairness"]:
                eod = abs(data["fairness"]["race"].get("equalized_odds_difference", 0))

                if eod > 0.10:
                    findings.append(
                        f"{model} on {dataset} exhibits fairness concerns "
                        f"(EOD={eod:.3f} across racial groups)"
                    )

    return findings


def generate_results_section(results: Dict) -> str:
    """Generate complete Results section for manuscript."""

    sections = []

    sections.append("## Results\n")
    sections.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d')}*\n")

    # Overall summary
    total_datasets = len([d for d in results if results[d]])
    total_models = sum(len(models) for models in results.values())

    sections.append(f"We evaluated {total_models} model configurations across {total_datasets} datasets. ")
    sections.append("Below we report performance, calibration, and fairness metrics for each dataset.\n")

    # Per-dataset results
    for dataset in ["compas", "communities_crime", "ncvs", "fbi_ucr"]:
        if dataset not in results or not results[dataset]:
            continue

        sections.append(f"### {dataset.replace('_', ' ').title()}\n")

        # Performance table
        sections.append("**Performance Metrics:**\n")
        sections.append(generate_performance_table(results, dataset))
        sections.append("\n")

    # Key findings
    sections.append("### Key Findings\n")

    findings = generate_key_findings(results)
    if findings:
        for i, finding in enumerate(findings, 1):
            sections.append(f"{i}. {finding}\n")
    else:
        sections.append("*Run experiments to populate key findings.*\n")

    sections.append("\n")

    return "\n".join(sections)


def generate_discussion_section(results: Dict) -> str:
    """Generate Discussion section outline with key points."""

    sections = []

    sections.append("## Discussion\n")

    sections.append("### Interpretation of Findings\n")
    sections.append("*Discuss what the results mean in context of research questions:*\n")
    sections.append("- **RQ1 (Performance):** Did domain adaptation improve predictions?\n")
    sections.append("- **RQ2 (Calibration & Fairness):** How well-calibrated and fair are the models?\n")
    sections.append("- **RQ3 (Robustness):** Are gains stable across contexts?\n")
    sections.append("\n")

    sections.append("### Comparison to Prior Work\n")
    sections.append("*Compare to literature:*\n")
    sections.append("- Dressel & Farid (2018): Simple models match COMPAS (AUROC ~0.70)\n")
    sections.append("- Rudin et al. (2020): Interpretable models for criminal justice\n")
    sections.append("- How do TabPFN results compare?\n")
    sections.append("\n")

    sections.append("### Policy Implications\n")
    sections.append("*Discuss practical implications:*\n")
    sections.append("- Should TabPFN be used in criminal justice settings?\n")
    sections.append("- What safeguards are needed for deployment?\n")
    sections.append("- How to address fairness concerns?\n")
    sections.append("- Role of human oversight and appeals processes\n")
    sections.append("\n")

    sections.append("### Limitations\n")
    sections.append("*Key limitations to acknowledge:*\n")
    sections.append("- Dataset scope and generalizability\n")
    sections.append("- Recidivism definition (re-arrest vs. conviction)\n")
    sections.append("- Missing counterfactuals (unobserved outcomes)\n")
    sections.append("- Ethical concerns with predictive policing\n")
    sections.append("\n")

    return "\n".join(sections)


def update_manuscript(
    manuscript_path: Path,
    results_section: str,
    discussion_section: str,
    backup: bool = True,
):
    """Update manuscript with results and discussion."""

    if not manuscript_path.exists():
        logger.error(f"Manuscript not found: {manuscript_path}")
        return

    # Read existing manuscript
    with open(manuscript_path, 'r') as f:
        content = f.read()

    # Backup original
    if backup:
        backup_path = manuscript_path.with_suffix('.md.bak')
        with open(backup_path, 'w') as f:
            f.write(content)
        logger.info(f"Created backup: {backup_path}")

    # Find Results section
    results_start = content.find("## Results")
    results_end = content.find("## Discussion")

    if results_start == -1:
        logger.warning("Could not find '## Results' section in manuscript")
        # Append to end
        new_content = content + "\n\n" + results_section
    elif results_end == -1:
        # Replace from Results to end
        new_content = content[:results_start] + results_section
    else:
        # Replace Results section
        new_content = content[:results_start] + results_section + content[results_end:]

    # Find Discussion section
    discussion_start = new_content.find("## Discussion")
    discussion_end = new_content.find("## References")

    if discussion_start == -1:
        # Append Discussion
        new_content = new_content + "\n\n" + discussion_section
    elif discussion_end == -1:
        # Replace from Discussion to end
        new_content = new_content[:discussion_start] + discussion_section
    else:
        # Replace Discussion section
        new_content = new_content[:discussion_start] + discussion_section + new_content[discussion_end:]

    # Write updated manuscript
    with open(manuscript_path, 'w') as f:
        f.write(new_content)

    logger.info(f"Updated manuscript: {manuscript_path}")


def generate_results_summary(results: Dict, output_file: Path):
    """Generate human-readable summary of all results."""

    lines = []

    lines.append("=" * 80)
    lines.append("EXPERIMENTAL RESULTS SUMMARY")
    lines.append("=" * 80)
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    for dataset, models in results.items():
        if not models:
            continue

        lines.append(f"\n{dataset.upper()}")
        lines.append("-" * 80)

        for model_name, data in models.items():
            lines.append(f"\n{model_name}:")

            if "metrics" in data:
                lines.append("  Performance:")
                for metric, value in data["metrics"].items():
                    lines.append(f"    {metric}: {value:.4f}")

            if "calibration" in data:
                lines.append("  Calibration:")
                for metric, value in data["calibration"].items():
                    lines.append(f"    {metric}: {value:.4f}")

            if "fairness" in data:
                lines.append("  Fairness:")
                for sensitive_attr, fair_metrics in data["fairness"].items():
                    lines.append(f"    {sensitive_attr}:")
                    for metric, value in fair_metrics.items():
                        if isinstance(value, (int, float)):
                            lines.append(f"      {metric}: {value:.4f}")

    lines.append("\n" + "=" * 80)

    summary_text = "\n".join(lines)

    # Write to file
    with open(output_file, 'w') as f:
        f.write(summary_text)

    logger.info(f"Saved results summary to {output_file}")

    return summary_text


def main():
    parser = argparse.ArgumentParser(description="Populate manuscript with results")
    parser.add_argument("--results", type=Path, default=Path("experiments/results"),
                       help="Results directory")
    parser.add_argument("--manuscript", type=Path, default=Path("paper/manuscript_draft.md"),
                       help="Manuscript file to update")
    parser.add_argument("--output", type=Path, default=Path("paper"),
                       help="Output directory for generated sections")
    parser.add_argument("--no-backup", action="store_true",
                       help="Don't create backup of manuscript")

    args = parser.parse_args()

    logger.info("=" * 80)
    logger.info("MANUSCRIPT POPULATION")
    logger.info("=" * 80)
    logger.info(f"Results directory: {args.results}")
    logger.info(f"Manuscript: {args.manuscript}")

    # Load all results
    logger.info("\nLoading experimental results...")
    results = load_all_results(args.results)

    if not any(results.values()):
        logger.warning("No experimental results found!")
        logger.info("\nTo generate results, run:")
        logger.info("  python experiments/run_experiment.py --dataset compas --models all")
        logger.info("\nFor now, creating template sections...")

    # Generate sections
    logger.info("\nGenerating Results section...")
    results_section = generate_results_section(results)

    logger.info("Generating Discussion section...")
    discussion_section = generate_discussion_section(results)

    # Save standalone sections
    args.output.mkdir(parents=True, exist_ok=True)

    results_file = args.output / "results_section.md"
    with open(results_file, 'w') as f:
        f.write(results_section)
    logger.info(f"Saved Results section to {results_file}")

    discussion_file = args.output / "discussion_section.md"
    with open(discussion_file, 'w') as f:
        f.write(discussion_section)
    logger.info(f"Saved Discussion section to {discussion_file}")

    # Update manuscript
    if args.manuscript.exists():
        logger.info(f"\nUpdating manuscript: {args.manuscript}")
        update_manuscript(
            args.manuscript,
            results_section,
            discussion_section,
            backup=not args.no_backup,
        )
    else:
        logger.warning(f"Manuscript not found: {args.manuscript}")

    # Generate summary
    summary_file = args.results / "summary.txt"
    logger.info(f"\nGenerating results summary...")
    summary = generate_results_summary(results, summary_file)

    logger.info("\n" + "=" * 80)
    logger.info("MANUSCRIPT POPULATION COMPLETE")
    logger.info("=" * 80)
    logger.info("\nGenerated files:")
    logger.info(f"  - {results_file}")
    logger.info(f"  - {discussion_file}")
    logger.info(f"  - {summary_file}")
    if args.manuscript.exists():
        logger.info(f"  - {args.manuscript} (updated)")


if __name__ == "__main__":
    main()
