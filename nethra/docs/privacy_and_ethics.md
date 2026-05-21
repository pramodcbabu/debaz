# Nethra: Ethics & Privacy by Design (MRP)

## 1. Privacy by Design: The MRP Advantage
Nethra utilizes **Multilevel Regression and Poststratification (MRP)** as its primary ethical safeguard. By architectural design, MRP eliminates the need for individual-level tracking and surveillance.

*   **Bucket-Level Scoring:** The intelligence engine operates entirely on demographic buckets (strata). It does not identify "Who" is a swing voter, but rather "What Demographic Profile" is currently volatile in a specific region.
*   **Anonymized Targeting:** Campaign interventions are deployed by targeting demographic segments on ad platforms, rather than uploading lists of individual hashed IDs.

---

## 2. Ethical Data Engineering: Data Minimization
We adhere to a strict policy of **Data Minimization** to comply with the **DPDP Act**.

1.  **Count-Based Ingestion:** We ingest only demographic *counts* from public voter rolls. Individual PII (Names, Phone Numbers) is never processed by the Nethra scoring engine.
2.  **Zero-PII Analytics:** The analytics database contains only aggregate demographic cells (e.g., "Males, 18-25, Booth 04") and their associated volatility scores.
3.  **Automated Deletion:** Any temporary files used during the ingestion of public records are cryptographically shredded immediately following the generation of the Poststratification Frame.

---

## 4. Human-in-the-Loop (HITL) for Interventions
While the engine identifies *who* to target, we mandate human review for *how* they are targeted.

*   **Approval Gate:** No intervention (ad, message, or campaign) is ever deployed to an external API without an explicit "Approved" flag from a human operator in the IT Cell.
*   **Auditability:** Every intervention has a persistent ID linked to the model version and the human approver, ensuring total accountability for the campaign's ethical footprint.

---

## 5. Security & Sovereignty
*   **Self-Custody:** All data (hashed or raw) remains within the political party's owned cloud infrastructure.
*   **Zero Data Brokering:** Nethra is a closed-loop intelligence system. No data is ever sold or shared with third-party brokers.
