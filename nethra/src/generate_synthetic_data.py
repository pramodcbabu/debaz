import pandas as pd
import numpy as np
from pathlib import Path

# Ensure data directory exists
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Synthetic poststratification frame (booth-level demographic cells)
np.random.seed(42)
num_booths = 50
booth_ids = [f"BOOTH_{i:03d}" for i in range(1, num_booths + 1)]
age_groups = ["18-30", "31-45", "46-60", "60+"]
genders = ["M", "F"]
social_groups = ["SC", "ST", "OBC", "General"]

rows = []
for booth in booth_ids:
    for age in age_groups:
        for gender in genders:
            for sg in social_groups:
                n_voters = np.random.randint(20, 200)
                rows.append({
                    "booth_id": booth,
                    "age_group": age,
                    "gender": gender,
                    "social_group": sg,
                    "n_voters": n_voters,
                })
post_df = pd.DataFrame(rows)
post_df.to_csv(DATA_DIR / "poststratification_frame.csv", index=False)

# Synthetic booth covariates (HV, HM, etc.)
booth_cov = pd.DataFrame({
    "booth_id": booth_ids,
    "historical_volatility_index": np.random.rand(num_booths),
    "historical_margin_of_victory": np.random.rand(num_booths) * 0.3,  # between 0 and 30%
    "wealth_index": np.random.rand(num_booths),
})
booth_cov.to_csv(DATA_DIR / "booth_covariates.csv", index=False)

print("Synthetic data generated in", DATA_DIR)
