# Nethra: Behavioral Data Science & Feature Engineering

## 1. Pivot: From Content to Mathematical Features
In the Nethra Engine, **Behavioral Psychology** is not just for generating ad scripts; it is a core component of the **Mathematical Model**. We convert cognitive biases and behavioral traits into quantifiable **Features** that predict the probability of a voter swinging.

---

## 2. Quantifying Cognitive Biases
For the Phase 1 prototype, we focus on the **$\gamma$ multiplier** (Behavioral Susceptibility) applied to local issues.

### A. The Loss Aversion Index ($\gamma = 1.8$)
*   **Feature Logic:** We categorize issues based on whether they represent a perceived loss (e.g., price hikes, tax increases) or a potential gain (e.g., new infrastructure).
*   **Impact on Math:** Issues categorized under Loss Aversion receive a 1.8x weight in the Propensity Score calculation, as behavioral data shows voters are significantly more volatile when facing perceived losses.

### B. Group-Identity Saliency ($\gamma = 1.4$)
*   **Feature Logic:** Individuals show higher susceptibility to issues that impact their primary in-group (e.g., communal, regional, or linguistic groups).
*   **Impact on Math:** If an issue is flagged as "Identity-Critical," it receives a higher multiplier, increasing the probability that voters in those demographics will be identified as "Moveable."

---

## 3. Modeling Behavioral Susceptibility
We calculate a **Behavioral Susceptibility Score** for various cohorts by analyzing historical data:
1.  **Reaction to Economic Shocks:** Analyzing how a booth's vote share shifted in the election immediately following a major economic policy change.
2.  **Engagement Volatility:** Analyzing the variance in social sentiment engagement for different framing styles (Fear vs. Hope).

### Feature: `psych_multiplier`
This column in our data schema reflects the individual's modeled reaction to the primary local issue.

| Issue Category | Behavioral Mechanism | Weight ($\gamma$) |
| :--- | :--- | :--- |
| Price Hike / Tolls | **Loss Aversion** | 1.8 |
| New Job Parks | **Future Discounting** | 1.0 |
| Cultural Identity | **In-Group Favoritism** | 1.4 |
| Local Crime/Safety | **Salience Bias** | 1.6 |

---

## 4. Behavioral Testing (Production)
In Track 2, we validate these weights using micro-surveys and digital engagement metrics, iteratively adjusting the $\gamma$ multipliers to improve the accuracy of the $P_s$ (Propensity Score) over time.
