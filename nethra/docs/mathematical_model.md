# Nethra: The Mathematical Foundation (MRP)

## 1. The Core Methodology: Multilevel Regression & Poststratification (MRP)
The Nethra intelligence engine utilizes **Multilevel Regression and Poststratification (MRP)** to accurately identify the "moveable middle" within a constituency. Unlike traditional polling, MRP allows us to project high-fidelity swing probabilities at the granular booth level using a combination of survey data and public demographic records.

---

## 2. Step 1: The Multilevel Model (The Training Phase)
We first train a Bayesian hierarchical model to learn the relationship between demographic characteristics and political volatility.

### The Regression Equation
$$ P(\text{Swing}_{i}) = \text{logit}^{-1}(\beta_0 + \alpha_{\text{age}[i]} + \alpha_{\text{gender}[i]} + \alpha_{\text{income}[i]} + \dots + \gamma_{\text{booth}[i]}) $$

*   **$\alpha$ (Demographic Effects):** These parameters represent the learned swing probability for a specific demographic "bucket" or **stratum** (e.g., Males aged 18-25).
*   **$\gamma$ (Geographic Effects):** A random effect that captures booth-level variation that demographics alone cannot explain (e.g., a specific local grievance like a closed factory).
*   **Behavioral Weighting:** Cognitive multipliers (like the **Loss Aversion Index**) are integrated as priors in the Bayesian model, increasing the starting probability of volatility for demographics exposed to specific negative economic shifts.

---

## 3. Step 2: Poststratification (The Projection Phase)
Once we have learned the swing probabilities for every demographic stratum, we "poststratify" them across the actual population counts of the constituency.

### Booth-Level Volatility Calculation
$$ V_{\text{booth}} = \sum_{k=1}^{K} (N_{\text{booth}, k} \cdot \hat{P}_k) $$

*   **$K$:** The total number of demographic strata (cells).
*   **$N_{\text{booth}, k}$:** The number of voters in Booth $X$ belonging to stratum $k$ (derived from ECI Voter Rolls and Census data).
*   **$\hat{P}_k$:** The predicted swing probability for stratum $k$ from our Multilevel Model.

**Outcome:** We generate a highly accurate projection of exactly how many "moveable" voters exist in every booth, without ever needing to violate the secrecy of the individual ballot.

---

## 4. Model Calibration & Anomaly Detection
We utilize private party data (Cadre reports) to calibrate the model's Bayesian priors and detect ground-level anomalies.

*   **Calibration:** If internal party data shows a high historical baseline for a specific demographic, that information is used to set the initial $\beta_0$ parameter.
*   **Anomaly Scoring:** The engine identifies booths where the predicted volatility ($V_{\text{booth}}$) significantly diverges from the cadre's reported support.
    $$ \text{Anomaly Score} = |V_{\text{booth}} - \text{Cadre_Reported_Support}| $$
    Large deltas provide leadership with objective, data-backed insights into potentially inaccurate ground reports.
