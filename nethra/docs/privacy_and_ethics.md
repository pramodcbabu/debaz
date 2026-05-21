# Nethra: Ethics & Algorithmic Fairness

## 1. Ethics in the Mathematical Model
Ethics in Nethra is not an afterthought; it is a **Constraint** built into our algorithms. We focus on two core pillars: **Data Minimization** and **Algorithmic Fairness**.

---

## 2. Algorithmic Fairness: Avoiding Redlining
Political micro-targeting often risks reinforcing social biases by ignoring or redlining certain demographic groups.

*   **The Mandate:** The model must identify the "Moveable Middle" based on individual propensity, not by using protected demographic classes (e.g., religion, caste) as primary predictive features.
*   **The Constraint:** We apply a **Demographic Parity** check to our $P_s$ scores. If the model identifies swing voters with a disproportionate demographic bias that cannot be explained by historical volatility or issue affinity, the weights are automatically adjusted to ensure equitable visibility across all cohorts.
*   **The Goal:** To provide the political client with a "True Map" of opportunity, not a biased one.

---

## 3. Ethical Data Engineering: Minimization
We adhere to the principle of **Data Minimization** to ensure voter privacy and comply with the **DPDP Act**.

1.  **Feature Selection:** We only ingest demographic proxies (e.g., age bracket, broad income bands) rather than granular personal histories.
2.  **Transient PII:** Personal Identifiable Information (Names, Phone Numbers) is used ONLY for the initial hashing and scoring process.
3.  **The Automated Deletion Pipeline:** Once the `voter_id_hash` and `p_swing` are generated, the raw source record is purged from the environment. The resulting "Intelligence Dataset" contains no raw PII.

---

## 4. Human-in-the-Loop (HITL) for Interventions
While the engine identifies *who* to target, we mandate human review for *how* they are targeted.

*   **Approval Gate:** No intervention (ad, message, or campaign) is ever deployed to an external API without an explicit "Approved" flag from a human operator in the IT Cell.
*   **Auditability:** Every intervention has a persistent ID linked to the model version and the human approver, ensuring total accountability for the campaign's ethical footprint.

---

## 5. Security & Sovereignty
*   **Self-Custody:** All data (hashed or raw) remains within the political party's owned cloud infrastructure.
*   **Zero Data Brokering:** Nethra is a closed-loop intelligence system. No data is ever sold or shared with third-party brokers.
