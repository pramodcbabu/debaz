# Nethra Project Strategic Operating Manual

This document defines the foundational mandates and operational workflows for project **Nethra**.

## 1. The 5-Perspective Mandate
Every plan, architectural decision, and feature review MUST explicitly address the following five perspectives:
1.  **Political Leadership & IT Cell:** Focus on Analytical Intelligence, ROI, and Anomaly Detection.
2.  **ML / Data Engineering:** Focus on **Multilevel Regression and Poststratification (MRP)** and Feature Engineering.
3.  **Behavioral Psychology:** Focus on **Quantifiable Traits** (multipliers $\gamma$) and Behavioral Priors.
4.  **Ethics & Data Privacy:** Focus on **Privacy by Design**, Data Minimization, and HITL Safeguards.
5.  **Product Management (PM):** Focus on Scope Control, Data Science Rigor, and implementation readiness.
Every plan, revision, and documentation review MUST maintain a professional, neutral, and objective tone. Simple enough for the client to follow, but technically deep for the engineering team. Avoid dramatic or sensationalist terminology.

## 2. Product Management Mandate: Dual-Track Execution
- **Track 1 (The ML Prototype):** Prioritize mathematical precision and demographic-level scoring.
    - **Tech Stack:** Streamlit, Plotly, Python, Static Synthetic CSVs.
    - **Zero-Friction:** No complex database infra; focus on the MRP core.
- **Track 2 (The Production Vision):** Scalable, cloud-native architecture (AWS, ClickHouse, Kafka) for real-world ingestion.

## 3. Project Core Mandates (The Nethra Essence)
- **MRP Engine:** The primary goal is to project booth-level swing counts using the MRP framework.
- **Behavioral Math:** Psychology must be integrated into the regression model as **Mathematical Priors**.
- **Privacy by Design:** The model must operate on demographic counts from public voter rolls, ensuring 100% DPDP Act compliance.
- **Ethics Gate:** Strict Human-in-the-Loop approval required for all campaign interventions.

## 4. Gemini-CLI Workflows
- **Scaffolding:** Gemini-CLI is authorized to autonomously scaffold the Streamlit UI and generate the **Synthetic Poststratification Frames** (`poststratification_frame.csv`).
- **Modularity:** Keep the MRP scoring logic decoupled from the UI for clarity and testability.
- **Data Integrity:** The `/data/` directory will store the simulated demographic strata features.

## 5. LaTeX & Markdown Quality Gate
- **Zero LaTeX Errors:** Every LaTeX equation must be thoroughly checked for syntax errors. 
- **Inline Math Syntax:** Never use spaces immediately after the opening `$` or immediately before the closing `$`. Always write `$equation$` instead of `$ equation $`.
- **Block Math Syntax:** Use standard GitHub mathematical blocks:
  $$
  equation
  $$
  without empty lines inside the LaTeX content, ensuring clean rendering on GitHub.
- **Verification:** Before pushing any documentation to GitHub, the agent must inspect the LaTeX syntax to guarantee 100% successful rendering on GitHub's native markdown processor.

