# Nethra Project Strategic Operating Manual

This document defines the foundational mandates and operational workflows for project **Nethra**, a Political AI Engine.

## 1. Project Core Mandates
- **Documentation Precedence:** No implementation of core AI logic or data pipelines shall occur without corresponding approved documentation in the `docs/` folder.
- **Privacy First:** All Voter PII (Specifically Phone Numbers) must be hashed using SHA-256 before being stored or transmitted to external ad platforms.
- **Verification over Assumption:** Every intervention strategy must be backed by the Causal Inference (Treatment vs. Control) methodology documented in `docs/mathematical_model.html`.
- **Dirty Data Zero Tolerance:** All incoming cadre reports must pass through the AI Anomaly Detection filter before influencing the Booth Volatility Index.

## 2. Operational Workflows
1. **Research & Simulation:** Before targeting a new region (e.g., UP, AP, or TN), mirroring of public ECI data must be completed.
2. **Review Cycle:** Any change to the `mathematical_model.html` or `survey_design_engine.html` requires a "Brutal Analysis" session with the Project Lead.
3. **Data Integrity:** The `/data/` directory is partitioned into `/data/public/` (mirrored truth) and `/data/simulated/` (synthetic private signals). Never mix real voter sentiment with simulated data in the same pipeline without explicit flagging.

## 3. Tech Stack Constraints
- **Backend:** FastAPI for high-concurrency API needs.
- **Targeting:** Meta Custom Audiences and Google Customer Match for phone-number based targeting.
- **LLM Usage:** Prompt engineering must prioritize political neutrality during data collection (Surveys) and high-velocity virality during intervention (Ad Scripting).
