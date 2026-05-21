# Nethra Command Center: Visualization Specs

## 1. Prototype UI Strategy (Strategic Command Interface)
The prototype UI is designed to demonstrate **Analytical Intelligence** over content generation. It focuses on visualizing the distribution of individual propensity scores and the fairness of the underlying model.

*   **Tech Stack:** Streamlit (Frontend), PyDeck (Geospatial Mapping), Plotly (ML Distribution Plots).
*   **Aesthetic:** Dark Mode primary, high-contrast markers for "Swing Probability."

---

## 2. Visual Mockups

### Mockup 1: The Macro View (Booth Propensity Distribution)
*Goal: Identify which booths have the highest concentration of volatile individuals.*

```text
+-------------------------------------------------------------+
| NETHRA COMMAND CENTER | [Override] SILENT PERIOD DEPLOYMENT HALT |
+-------------------------------------------------------------+
|                                                             |
|   [ 3D HEX-BIN MAP OF DISTRICT ]                            |
|   (Height = Mean Propensity Score $P_s$)                    |
|   (Color = Voter Density)                                   |
|                                                             |
+-------------------------------------------------------------+
| DISTRICT INTELLIGENCE:                                      |
| [ Avg P_s: 0.62 ] [ Fairness Score: 0.94 ] [ Anomalies: 12 ] |
+-------------------------------------------------------------+
```

### Mockup 2: The Individual Deep-Dive (Sidebar)
*Goal: Display the features and constraints behind the booth's identification.*

```text
+-----------------------+---------------------------------------+
|  ML MODEL EXPLAINER   | SELECTED: AC-125 BOOTH 04             |
+-----------------------+---------------------------------------+
| Swing Probability Map:| TOP FEATURES IN MODEL:                |
| [ Distribution Plot ] | 1. [Loss Aversion Index] (Weight: 1.8)|
| (Bell curve showing   | 2. [Historical Volatility] (Weight: 1.2)|
|  voter propensity)    | 3. [Issue Affinity]      (Weight: 0.9)|
+-----------------------+---------------------------------------+
| [!] FAIRNESS AUDIT:                                           |
| Demographic Parity Check: PASSED                              |
| (No systemic bias detected across age/income groups)          |
+-----------------------+---------------------------------------+
```

### Mockup 3: The Intervention (The Generator)
*Goal: Demonstrate the transition from analytical intelligence to ethically-vetted cohort targeting.*

```text
+-------------------------------------------------------------+
| [ GENERATE TARGETED INTERVENTION ]                          |
+-------------------------------------------------------------+
| SOURCE STRATA: Male, 18-25, Other-Worker                    |
| TARGET LOCATION: AC-125 Booth 04 (Pin: 600028)              |
| PSYCH FRAME: Loss Aversion (High Salience: Toll Fees)       |
+-------------------------------------------------------------+
| INTERVENTION PREVIEW (AI GENERATED):                        |
| "Namaste Booth 04! Fed up of the toll prices? [Candidate]   |
| has a plan to fix the infrastructure..."                    |
+-------------------------------------------------------------+
| [X] I certify this matches the demographic cohort filter.   |
| [ APPROVE & DEPLOY TO META ] [ REGENERATE ] [ EXPORT ]      |
+-------------------------------------------------------------+
```

---

## 3. Visual Components for ML Team
*   **`st.pydeck_chart`**: Renders 3D bins using `avg_p_swing` from `mock_constituencies.csv`.
*   **`st.plotly_chart`**: Used to show histograms of individual `p_swing` scores within a selected booth.
*   **`st.metric`**: Displays the `fairness_metric` and `anomaly_score`.
