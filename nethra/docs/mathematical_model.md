# Nethra: The Mathematical Foundation (MRP)

## 1. The Core Methodology: Multilevel Regression & Poststratification (MRP)
The Nethra intelligence engine utilizes **Multilevel Regression and Poststratification (MRP)** to accurately identify the "moveable middle" within a constituency. Unlike traditional polling, MRP allows us to project high-fidelity swing probabilities at the granular booth level using a combination of survey data and public demographic records.

---

## 2. Step 1: The Multilevel Model (The Training Phase)
We first train a Bayesian hierarchical model to learn the relationship between demographic characteristics and political volatility.

### The Regression Equation
$$ P(\text{Swing}_i) = \text{logit}^{-1}(\beta_0 + \alpha_{\text{age},i} + \alpha_{\text{gender},i} + \alpha_{\text{social\_cat},i} + \alpha_{\text{occupation},i} + \gamma_{\text{booth},i}) $$

*   **$\alpha$ (Demographic Strata Parameters):** These are the learned swing probabilities for every combination of age, gender, social category, and occupation. 
*   **Behavioral Weighting:** Cognitive multipliers (like the **Loss Aversion Index**) are integrated as priors in the Bayesian model, increasing the starting probability of volatility for demographics exposed to specific negative economic shifts.
*   **Bayesian Shrinkage:** The model handles "sparse" buckets (e.g., a bucket with only 2 voters) by mathematically shrinking the estimate toward the broader demographic mean, ensuring model stability.

---

## 3. Step 2: Poststratification (The Projection Phase)
Once we have learned the swing probabilities for every demographic stratum ($k$), we project them across the actual population counts of the constituency.

### Booth-Level Volatility Calculation ($V_{\text{booth}}$)
$$ V_{\text{booth}} = \sum_{k=1}^{96} (N_{booth, k} \cdot \hat{P}_k) $$

*   **$N_{booth, k}$:** The number of voters in Booth $X$ belonging to demographic stratum $k$ (derived from ECI Voter Rolls and Census data).
*   **$\hat{P}_k$:** The predicted swing probability for stratum $k$ from our Multilevel Model.

---

## 4. From Math to Action: Cohort Ad Targeting
A strategic advantage of the MRP framework is its ability to drive hyper-localized interventions without individual PII. We utilize **Demographic Cohort Targeting** (Segment Targeting).

### The Strategic Shift
Instead of uploading a list of individual phone numbers (Custom Audiences), Nethra provides the ad platforms (Meta/Google) with the exact demographic and geographic parameters of the highly volatile strata.

### Example: Targeting High-Volatility Strata $k$
If the model identifies that **Strata $k$ (Males, 18-25, Low Income)** in **Booth 04** has a 75% swing probability, the IT Cell approves a deployment with the following parameters:

*   **Geographic Filter:** Pin Code matching Booth 04 (e.g., `600028`).
*   **Demographic Filter:** Gender: `Male`, Age: `18-25`.
*   **Interest/Socio-Economic Filter:** `Low Income Proxy` (derived from platform-native interest categories matching census profiles).

**Outcome:** The ad platform's internal algorithm identifies the individuals matching these exact parameters and serves them the campaign, achieving micro-targeting precision while maintaining absolute privacy.

---

## 5. Model Calibration & Anomaly Detection
We utilize private party data (Cadre reports) to calibrate the model's Bayesian priors and detect ground-level anomalies.

*   **Calibration:** If internal party data shows a high historical baseline for a specific demographic, that information is used to set the initial $\beta_0$ parameter.
*   **Anomaly Scoring:** The engine identifies booths where the predicted volatility ($V_{\text{booth}}$) significantly diverges from the cadre's reported support.
    $$ \text{Anomaly Score} = |V_{\text{booth}} - \text{Cadre Reported Support}| $$
