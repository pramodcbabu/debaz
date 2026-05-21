# Nethra: Behavioral Psychology & Influence Strategy

## 1. The Behavioral Data Science Mandate
Nethra does not just identify voters; it seeks to understand the cognitive drivers of their decisions. By applying behavioral science to demographic and issue data, we can create content that resonates at a primal level.

## 2. Core Framework: Pragmatic Cognitive Framing
For the Phase 1 prototype, we focus on three high-impact cognitive biases to influence the "Moveable Middle":

### A. Loss Aversion vs. Gain Framing
*   **The Science:** Humans are twice as sensitive to potential losses as they are to equivalent gains.
*   **Application:** If the top issue is "Youth Unemployment," the AI generates two frames:
    *   *Gain Frame:* "Vote for [Candidate] to bring 10,000 new jobs."
    *   *Loss Frame:* "Stop the opposition from taking away your family's financial future."
*   **Recommendation:** Default to Loss Aversion for maximum impact in volatile booths.

### B. Issue Salience & Emotional Priming
*   **The Science:** People vote based on the issues that are most "top of mind" (salient) at the moment of decision.
*   **Application:** The `I_salience` score in the mathematical model determines the "Prime Topic." The behavioral engine then "primes" the voter with localized imagery and language specific to that grievance (e.g., using regional dialects for water supply issues).

### C. In-Group Favoritism (Hyper-Localization)
*   **The Science:** Voters are more likely to trust messages that feel "local" and reflect their immediate social group.
*   **Application:** The AI generates scripts that reference specific local landmarks, booth-level problems, and communal identities, making the "War Room" messaging feel like a "Neighbor-to-Neighbor" conversation.

---

## 3. The Behavioral Feedback Loop
In the production vision, Nethra tracks engagement metrics (click-through rates, video watch time) across different psychological frames.

| Frame | Engagement Rate | Result |
| :--- | :--- | :--- |
| Loss Aversion | 4.2% | **Primary Frame** for Booth X |
| Gain Framing | 1.8% | Deprioritize |
| Community Pride | 3.1% | Secondary Frame |

---

## 4. Algorithmic Prompt Engineering (Behavioral)
The LLM prompt is structured to include:
1.  **Target Identity:** (e.g., "Young first-time voter in semi-urban booth")
2.  **Primary Trigger:** (e.g., "Loss Aversion regarding toll road prices")
3.  **Local Context:** (e.g., "Mention the flyover project delay")
4.  **Action Bias:** (e.g., "Direct Call to Action: Vote on Monday to save your wallet.")
