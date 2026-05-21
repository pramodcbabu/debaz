# Data Engineering & Feature Architecture (MRP)

## 1. Prototype Strategy: The Poststratification Frame
For the Phase 1 prototype, we focus on constructing the **Poststratification Frame**. This frame represents the demographic census of every booth in the constituency.

### `poststratification_frame.csv` Schema (ML Input Layer)
| Column | Type | Data Source | Description |
| :--- | :--- | :--- | :--- |
| `booth_id` | STRING | ECI Voter Rolls | Unique ID for the booth |
| `stratum_id` | STRING | Derived | ID for the demographic cell (e.g., `M_18-25_LowInc`) |
| `voter_count` | INT | ECI / Census | Number of voters belonging to this stratum |
| `historical_base` | FLOAT | ECI Form 20 | Historical vote share for this booth |
| `est_swing_prob` | FLOAT | **MRP Model** | Predicted $\hat{P}_k$ for this stratum |

---

## 2. Data Ingestion & Transformation
Nethra's data engineering pipeline is divided into three distinct tracks to support the MRP architecture:

1.  **Public Track (The Frame):**
    *   **ECI Voter Rolls:** Provides age and gender distributions per booth.
    *   **Census Overlays:** Provides income and social category proxies for the booth geography.
2.  **External Track (The Sentiment):**
    *   **Social Listening:** Aggregated sentiment scores by demographic keywords to estimate the $\alpha$ parameters (swing probabilities) for each stratum.
3.  **Private Track (The Calibration):**
    *   **Cadre Interaction Logs:** Anonymized logs from ground apps (SARAL/Shakti) are used to adjust the **Bayesian Priors** of the Multilevel Model.

---

## 3. The Privacy-First ETL Pipeline
A core advantage of the MRP approach is the elimination of the need to store or process individual PII during the scoring phase.

1.  **Count-Based Ingestion:** We ingest only the *counts* of voters per demographic bucket from the ECI voter rolls.
2.  **Demographic Stratification:** We create a multidimensional matrix (the Frame) that represents all demographic combinations.
3.  **Result:** The final dataset used for visualization and strategy contains zero individual-level data, ensuring absolute compliance with the **DPDP Act**.

---

## 4. Transformed Output: `mock_constituencies.csv`
The individual stratum-level predictions are aggregated to provide the **Strategic Dashboard** view for leadership.

| Column | Type | Derivation |
| :--- | :--- | :--- |
| `booth_id` | STRING | Primary Key |
| `lat` / `lon` | FLOAT | Booth centroid coordinates |
| `predicted_swing_votes`| INT | Sum of $(N_k \cdot \hat{P}_k)$ for the booth |
| `volatility_index` | FLOAT | Normalized $V_{\text{booth}}$ score (0-1) |
| `top_issue_salience` | FLOAT | Aggregated $I_s$ including behavioral weights |
| `anomaly_score` | FLOAT | Delta between MRP prediction and Cadre reports |
