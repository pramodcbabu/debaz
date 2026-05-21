# Nethra: The Mathematical Foundation

## 1. The Core Objective: Individual Swing Propensity ($P_s$)
The essence of Nethra is to move from aggregate booth statistics to individual-level predictions. We calculate a **Propensity Score ($P_{s_i}$)** for every voter in the constituency.

### The Individual Propensity Model
$$ P_{s_i} = \sigma(\theta \cdot X_i) $$

Where:
*   **$X_i$:** A feature vector for voter $i$ containing demographic proxies, historical volatility, and issue affinity.
*   **$\sigma$:** The logistic function, mapping the score to a probability (0-1).
*   **$\theta$:** The weight vector learned from historical election data and sentiment shifts.

---

## 2. Behavioral Feature Engineering: The $\gamma$ Multiplier
**Behavioral Psychology** is integrated directly into the math as a weight multiplier for issue saliency. We don't just measure if a voter cares about an issue; we measure their **Psychological Susceptibility** to that issue's framing.

### Behavioral Salience ($I_{s_i}$)
$$ I_{s_i} = \sum_{j=1}^{n} (A_{ij} \cdot \omega_j \cdot \gamma_j) $$

*   **$A_{ij}$:** Affinity of voter $i$ to issue $j$.
*   **$\omega_j$:** Global saliency of issue $j$.
*   **$\gamma_j$ (The Behavioral Multiplier):** A weight assigned based on cognitive biases.
    *   *Loss Aversion Issues* (e.g., Toll Price Hikes): $\gamma = 1.8$
    *   *Gain Framing Issues* (e.g., New IT Parks): $\gamma = 1.0$
    *   *Identity/Pride Issues*: $\gamma = 1.4$

---

## 3. Ethical Constraints: Algorithmic Fairness
To prevent the model from systematically "redlining" or ignoring specific demographics (which is both an ethical and a political risk), we introduce a **Fairness Constraint** during the model optimization.

### Demographic Parity Constraint
$$ |P(P_s > \tau | D = a) - P(P_s > \tau | D = b)| < \epsilon $$

*   The difference in the probability of being identified as a "Swing Voter" ($P_s > \tau$) between any two demographic groups ($a, b$) must be less than a small threshold $\epsilon$. 
*   This ensures the AI engine identifies the *true* moveable middle, rather than just reinforcing existing social biases in the data.

---

## 4. Anomaly Detection: Ground Truth Validation
We use **Isolation Forests** to detect multi-dimensional outliers where ground reports from cadre ($C_{rep}$) significantly deviate from the predicted propensity distribution ($P_s$) and historical ECI baselines ($H_{base}$).

$$ \text{Anomaly Score}(i) = \text{IsolationForest}(C_{rep}, P_s, H_{base}) $$
*   High scores flag booths where local reports are likely "dirty" or inflated, protecting the leadership from making decisions based on false cadre optimism.
