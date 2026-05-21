# Data Engineering & Feature Architecture

## 1. Prototype Strategy: Synthetic Voter File
For the Phase 1 prototype, we will generate a **Synthetic Voter File** that represents the input for our propensity model. This file simulates the merging of public ECI data with private ground reports.

### `individual_voter_features.csv` Schema (ML Input Layer)
| Column | Type | Ethical Mandate | Description |
| :--- | :--- | :--- | :--- |
| `voter_id_hash` | STRING | **SHA-256** | Unique identifier (hashed raw phone/ID) |
| `age_proxy` | INT | Data Binning | Age bracket (e.g., 18-25, 26-35) |
| `income_proxy` | FLOAT | Privacy Masking | Modeled income level based on locality |
| `historical_volatility`| FLOAT | Feature Eng | Variance in booth's historical vote share |
| `issue_affinity_score` | FLOAT | Feature Eng | Probability of interest in prime local issue |
| `psych_multiplier` | FLOAT | **Behavioral** | $\gamma$ score based on issue category |
| `p_swing` | FLOAT | **Model Output** | The calculated individual propensity score |

---

## 2. The Data Minimization Pipeline (Ethical ETL)
To ensure compliance with the **DPDP Act** and ethical standards, Nethra employs a "Transient Ingestion" pipeline.

1.  **Ingestion:** Raw PII (Name, Phone) is ingested into an encrypted transient buffer.
2.  **Hashing & Scoring:** `voter_id_hash` is created and `p_swing` is calculated.
3.  **Shredding:** **All raw PII is cryptographically shredded immediately.** Only the hashed ID and the calculated features/scores remain in the analytics database.
4.  **Audit Trail:** Metadata (timestamps, model versions) is kept for accountability without exposing voter identities.

---

## 3. Transformed Output: `mock_constituencies.csv`
The individual scores are aggregated to provide the **War Room** view for leadership.

| Column | Type | Derivation |
| :--- | :--- | :--- |
| `booth_id` | STRING | Primary Key |
| `lat` / `lon` | FLOAT | Booth centroid coordinates |
| `swing_voter_count` | INT | Count of individuals where $P_s > 0.7$ |
| `avg_p_swing` | FLOAT | Mean propensity score of the booth |
| `fairness_metric` | FLOAT | Demographic parity score of the model in this booth |
| `top_issue_salience` | FLOAT | Aggregated $I_s$ (including behavioral weights) |

---

## 4. Production Data Sources
*   **ECI Public Data:** Historical results from CEO portals (Historical Volatility).
*   **Cadre APIs (SARAL/Shakti):** Ground disposition and issue engagement (Affinity Score).
*   **Social Listening:** Aggregated sentiment at the pin-code level (Global Saliency $\omega$).
