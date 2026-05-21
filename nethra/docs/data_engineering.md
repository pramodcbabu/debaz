# Data Engineering & Feature Architecture (MRP)

## 1. Prototype Strategy: The 96-Strata Frame
For the Phase 1 prototype, we construct a **Poststratification Frame** consisting of 96 demographic buckets (strata) per booth. This provides the optimal balance between political granularity and statistical stability.

### Strata Definition (The 96-Way Split)
The frame is calculated by multiplying the following categorical features:
1.  **Gender (ECI):** Male, Female (2)
2.  **Age (ECI):** 18-25, 26-35, 36-50, 50+ (4)
3.  **Social Category (Census):** SC, ST, General/OBC (3)
4.  **Economic/Occupation (Census):** Cultivator, Ag-Laborer, Other-Worker, Non-Worker (4)
*   **Total Strata per Booth:** $2 \times 4 \times 3 \times 4 = \mathbf{96 \text{ Buckets}}$

---

## 2. The Spatial Bridge Pipeline
Since ECI Electoral Rolls (Booth level) and Census Data (Village/Ward level) do not share common administrative boundaries, Nethra employs a **GIS Spatial Join** to bridge the datasets:

1.  **Booth Centroids:** We extract the Latitude/Longitude of the polling station from the ECI Form 20 or PDF metadata.
2.  **Census Overlay:** We perform a spatial point-in-polygon join to identify which Census Village/Ward boundary contains the booth.
3.  **Attribute Imputation:** We project the socio-economic proportions (Social Category, Occupation) of the Census area onto the known Age/Gender counts of the ECI Booth Roll.

---

## 3. Mathematical Viability & Privacy Gate
*   **Density Check:** In an average Indian booth (~900 voters), a 96-strata model yields an average of **~9.3 voters per bucket**. 
*   **k-Anonymity Filter:** Nethra enforces a strict $k \ge 10$ privacy threshold. If a bucket's voter count falls below 10, the data pipeline automatically merges it into the nearest logical demographic bucket (e.g., merging "Male, SC, 18-25, Cultivator" with "Male, SC, 26-35, Cultivator") until the threshold is met.
*   **Compliance:** This ensures zero individual-level tracking and total compliance with the **DPDP Act**.

---

## 4. Transformed Output: `mock_constituencies.csv`
| Column | Type | Derivation |
| :--- | :--- | :--- |
| `booth_id` | STRING | Primary Key |
| `lat` / `lon` | FLOAT | Booth centroid coordinates |
| `predicted_swing_votes`| INT | Sum of $(N_k \cdot \hat{P}_k)$ for the booth |
| `volatility_index` | FLOAT | Normalized $V_{\text{booth}}$ score (0-1) |
| `top_issue_salience` | FLOAT | Aggregated $I_s$ including behavioral weights |
| `anomaly_score` | FLOAT | Delta between MRP prediction and Cadre reports |
