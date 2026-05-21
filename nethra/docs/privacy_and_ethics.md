# Nethra: Ethics, Privacy & Compliance

## 1. The Compliance-Ethics Nexus
In Nethra, **Compliance** is the floor, but **Ethics** is the ceiling. We treat data privacy not just as a legal hurdle, but as a moral imperative to protect the democratic process.

*   **Legal Compliance (DPDP Act):** We utilize SHA-256 hashing and client-side encryption to ensure no PII is exposed to third-party platforms.
*   **Ethical Mirror:** This technical compliance serves the ethical goal of **Voter Sovereignty**. By ensuring PII is never stored or shared in its raw form, we prevent the creation of permanent, invasive surveillance profiles.

---

## 2. The Ethical "Red Lines" (Prohibited Actions)
To maintain the integrity of the election and the brand of the political client, the following actions are strictly prohibited:

1.  **Deepfakes & Synthetic Voices:** No AI-generated imagery or audio of real people (candidates or opponents) may be created. AI is used only for script generation and generic visual assets.
2.  **Voter Suppression:** No content may be generated with the intent to discourage a population from voting or provide false information about polling locations/times.
3.  **Identity Deception:** AI-generated content must not masquerade as personal communication from a real individual unless explicitly authorized and reviewed by that individual.

---

## 3. Truthful Contrast: The Ethical Boundary
Nethra adopts a **Truthful Contrast** policy.
*   **Permitted:** Generating hard-hitting ads that highlight an opponent's factual voting record, public statements, or failed policy outcomes.
*   **Prohibited:** Generating defamatory lies, unverified conspiracy theories, or ad-hominem attacks unrelated to public service.

---

## 4. Human-in-the-Loop (HITL) Mandate
**No AI-generated script or campaign is ever deployed automatically.**
*   The IT Cell acts as the "Ethical Gatekeeper."
*   Every output from the Gemini API must be manually reviewed and clicked "Approved" within the Nethra Command Center before being pushed to ad platforms.
*   This ensures a human agent is always responsible for the final message.

---

## 5. Data Sovereignty & The Kill Switch
*   **Sovereignty:** The political party maintains 100% legal and technical ownership of the raw data. Nethra is a tool, not a data broker.
*   **The Kill Switch:** A prominent red button in the UI halts all outbound API calls to ad platforms. This is mandated for use 48 hours before polling (The Silent Period) to comply with ECI regulations and ethical norms.
