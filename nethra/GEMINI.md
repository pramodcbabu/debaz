# Nethra Project Strategic Operating Manual

This document defines the foundational mandates and operational workflows for project **Nethra**.

## 1. The 5-Perspective Mandate
Every plan, architectural decision, and feature review MUST explicitly address the following five perspectives:
1.  **Political Leadership & IT Cell:** Focus on Analytical Intelligence, ROI, and Anomaly Detection.
2.  **ML / Data Engineering:** Focus on **Individual Propensity Modeling**, Feature Engineering, and Scalability.
3.  **Behavioral Psychology:** Focus on **Quantifiable Traits** ( multipliers $\gamma$) and Behavioral Susceptibility features.
4.  **Ethics & Data Privacy:** Focus on **Algorithmic Fairness**, Data Minimization, and HITL Safeguards.
5.  **Product Management (PM):** Focus on Scope Control, Data Science Rigor, and implementation readiness.

## 2. Product Management Mandate: Dual-Track Execution
- **Track 1 (The ML Prototype):** Prioritize mathematical precision and individual-level scoring.
    - **Tech Stack:** Streamlit, Plotly, Python, Static Synthetic CSVs.
    - **Zero-Friction:** No complex database infra; focus on the core intelligence engine.
- **Track 2 (The Production Vision):** Scalable, cloud-native architecture (AWS, ClickHouse, Kafka) for real-world ingestion.

## 3. Project Core Mandates (The Nethra Essence)
- **Individual Propensity:** The primary goal is to calculate individual **$P_s$ scores** and identify the "Moveable Middle."
- **Behavioral Math:** Psychology must be integrated into the math model as **Feature Weights**, not just content prompts.
- **Privacy & Fairness:** All Voter PII must be hashed using SHA-256. The model must pass an **Algorithmic Fairness Audit** to prevent demographic redlining.
- **Ethics Gate:** Strict Human-in-the-Loop approval required for all campaign interventions.

## 4. Gemini-CLI Workflows
- **Scaffolding:** Gemini-CLI is authorized to autonomously scaffold the Streamlit UI and generate the **Synthetic Voter Files** (`individual_voter_features.csv`).
- **Modularity:** Keep the propensity scoring logic decoupled from the UI for clarity and testability.
- **Data Integrity:** The `/data/` directory will store the simulated individual-level features.
