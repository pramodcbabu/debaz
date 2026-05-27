import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Paths
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load synthetic data
post_df = pd.read_csv(DATA_DIR / "poststratification_frame.csv")
booth_cov = pd.read_csv(DATA_DIR / "booth_covariates.csv")

# Simple analysis: average volatility and margin per booth
summary = booth_cov.groupby("booth_id").agg({
    "historical_volatility_index": "mean",
    "historical_margin_of_victory": "mean",
    "wealth_index": "mean"
}).reset_index()

# Merge with poststratification counts (total voters per booth)
voter_counts = post_df.groupby("booth_id")["n_voters"].sum().reset_index(name="total_voters")
summary = summary.merge(voter_counts, on="booth_id")

# Plot HV vs HM, sized by total voters
plt.figure(figsize=(8,6))
sc = plt.scatter(
    summary["historical_volatility_index"],
    summary["historical_margin_of_victory"],
    s=summary["total_voters"] * 0.5,
    c=summary["wealth_index"],
    cmap="viridis",
    alpha=0.7,
    edgecolor="k"
)
plt.xlabel("Historical Volatility Index (HV)")
plt.ylabel("Historical Margin of Victory (HM)")
plt.title("Booth‑level HV vs HM (size = voters, color = wealth)")
plt.colorbar(sc, label="Wealth Index")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plot_path = OUTPUT_DIR / "hv_vs_hm.png"
plt.savefig(plot_path, dpi=150)
plt.close()

# Write a simple markdown summary
md_path = Path(__file__).resolve().parent.parent / "docs" / "analysis_results.md"
with open(md_path, "w") as f:
    f.write("# Analysis Results\n\n")
    f.write(f"* Generated synthetic data for **{len(post_df)}** demographic rows.\n")
    f.write(f"* Processed **{len(booth_cov)}** booths.\n")
    f.write(f"* Plot saved to `{plot_path}`.\n\n")
    f.write("## Summary Statistics\n\n")
    f.write(summary.describe().to_markdown() + "\n")
    f.write("\n![HV vs HM Plot]({})\n".format(plot_path.relative_to(Path(__file__).resolve().parent.parent)))

print("Analysis complete. Results written to", md_path)
