# Nethra: The Mathematical Foundation

## 1. The Core Objective: Swing Voter Density ($S_d$)
The primary goal for both the **Political Leader** and the **ML Team** is to locate the "Moveable Middle." We calculate **Swing Voter Density ($S_d$)** at the booth level to determine where to deploy resources.

### Prototype Implementation: The Heuristic Model
$$ S_d = (\alpha \cdot M_{vol}) + (\beta \cdot I_{salience}) $$

*   **$M_{vol}$ (Historical Volatility):** Calculated from ECI Form 20 data ($1 - \text{victory margin}$). A thin margin suggests high volatility.
*   **$I_{salience}$ (Issue Saliency):** A weight (0-1) assigned to the intensity of local issues. This score is used by the **Behavioral Engine** to determine the primary emotional frame (e.g., High Salience + Negative Sentiment = Loss Aversion Frame).
*   **$S_d$:** Resulting density (0-1), powering the heatmap visualization.

---

## 2. Individual Identification: Deterministic Lookalike Pipeline
While $S_d$ identifies **where** the swing voters are, the **Deterministic Lookalike Pipeline** identifies **who** they are to enable micro-targeting.

### ML & Data Engineering Perspective: The Pipeline
1.  **Seed Audience Extraction:** We ingest PII (Phone/Email) from internal Cadre Apps (e.g., voters marked as "Undecided" or "Influential" by ground workers).
2.  **Privacy-Preserving Hashing:**
    *   **Action:** Apply `SHA-256` hashing to raw PII *before* it leaves the secure environment.
    *   **Logic:** `Hashed_ID = SHA256(Raw_Phone + Salt)`.
3.  **Platform Matching:** Upload `Hashed_ID` lists to Meta/Google Custom Audiences.
4.  **Lookalike Modeling ($L_m$):**
    $$ L_m = \text{Top } 1\% \text{ of users matching demographics/interests of the Seed Audience in Booth } X. $$

### Political & IT Cell Perspective: Security & Precision
*   **DPDP Compliance:** No raw PII is ever uploaded to ad platforms. The hashing is irreversible.
*   **Hyper-Precision:** Instead of spray-and-pray ads, the IT cell targets only those with a high mathematical propensity to swing, maximizing budget efficiency.

---

## 3. Causal Inference: ROI via Synthetic Control
To prove to leadership that Nethra is winning elections, we use the **Synthetic Control Method**.

*   **The Problem:** We cannot know what would have happened in Booth A if we *hadn't* run Nethra ads.
*   **The Solution:**
    1.  **Target Booth ($T$):** The booth receiving Nethra interventions.
    2.  **Synthetic Control ($C^*$):** A weighted combination of other booths that didn't receive ads but historically mirrored Booth T's voting patterns.
    3.  **Causal Impact:** $\Delta = \text{VoteShare}(T) - \text{VoteShare}(C^*)$.
*   **ROI Narrative:** "For every ₹1 spent on Nethra, we generated a $\Delta$ of 150 votes compared to the baseline."

---

## 4. Anomaly Detection (Ground Truth Validation)
Political cadre often inflate success reports to please leadership.

*   **Logic:** We flag booths where `Cadre_Report_Score` significantly deviates from the `Historical_Trend_Line` and `Social_Sentiment_Score`.
*   **Implementation:** Using **Isolation Forest** algorithms to detect multi-dimensional outliers, protecting leadership from "dirty data."
