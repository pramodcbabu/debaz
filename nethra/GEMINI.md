# Nethra Project Strategic Operating Manual

This document defines the foundational mandates and operational workflows for project **Nethra**.

## 1. The 5-Perspective Mandate
Every plan, architectural decision, and feature review MUST explicitly address the following five perspectives:
1.  **Political Leadership & IT Cell:** Focus on Business Value, ROI, and Actionable Intelligence for decision-makers.
2.  **ML / Data Engineering:** Focus on Technical Scalability, Data Schema Integrity, and Mathematical Rigor.
3.  **Behavioral Psychology:** Focus on Behavioral Data Science, Cognitive Framing (Loss Aversion), and Emotional Priming.
4.  **Ethics & Data Privacy:** Focus on the Compliance-Ethics Nexus, DPDP Act adherence, Truthful Contrast, and Human-in-the-Loop (HITL) safeguards.
5.  **Product Management (PM):** Focus on MVP Scope Control, Time-to-Market, and readiness for implementation.

## 2. Product Management Mandate: Dual-Track Execution
- **Track 1 (The Pitch Prototype):** Prioritize speed and visual impact for Business Development. 
    - **Tech Stack:** Streamlit, Python, Static CSV/JSON, Gemini API.
    - **Zero-Friction:** No complex infrastructure (Kafka, ClickHouse) or paid subscriptions during this phase.
- **Track 2 (The Production Vision):** Maintain the scalable, cloud-native architecture documentation to prove technical competence to client IT cells.

## 3. Project Core Mandates (The Nethra Essence)
- **Swing Focus:** The primary goal is to locate the **Swing Voter Population** and identify the **Key Issues** driving their volatility.
- **Intervention:** Every identified swing booth must have a corresponding AI-generated engagement campaign (Reels/Shorts scripts).
- **Privacy First (Production):** All Voter PII must be hashed using SHA-256 before storage or transmission to ad platforms.
- **Ethics First:** Strict adherence to "No Deepfakes" and "Human-in-the-Loop" approval for all AI outputs.

## 4. Gemini-CLI Workflows
- **Scaffolding:** Gemini-CLI is authorized to autonomously scaffold the Streamlit UI and generate the mock data files.
- **Modularity:** Keep the prototype logic in simple, modular Python files to minimize context usage and prevent "hallucination creep."
- **Data Integrity:** The `/data/` directory will be used for static mock data (`mock_constituencies.csv`) for the prototype.

## 5. License Compliance
- **Open Source:** All software used in the prototype (Streamlit, Pandas, PyDeck, etc.) must be 100% free and open-source (MIT/Apache 2.0). 
- **Zero Paid Subscriptions:** The prototype must not require the user to sign up for paid services (e.g., Twilio, AWS) for the demo to function.
