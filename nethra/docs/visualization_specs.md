# Nethra Command Center: Visualization Specs

## 1. Prototype UI Strategy (The War Room Aesthetic)
The prototype UI is designed to demonstrate **Analytical Intelligence** over content generation. It focuses on visualizing the distribution of individual propensity scores and the fairness of the underlying model.

*   **Tech Stack:** Streamlit (Frontend), PyDeck (Geospatial Mapping), Plotly (ML Distribution Plots).
*   **Aesthetic:** Dark Mode primary, high-contrast markers for "Swing Probability."

---

## 2. Visual Mockups

### Mockup 1: The Macro View (Booth Propensity Distribution)
*Goal: Identify which booths have the highest concentration of volatile individuals.*

```text
+-------------------------------------------------------------+
| NETHRA COMMAND CENTER | [Red Button] SILENT PERIOD KILL SWITCH |
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
*Goal: Show the transition from mathematical intelligence to approved action.*

```text
+-------------------------------------------------------------+
| [ GENERATE TARGETED INTERVENTION ]                          |
+-------------------------------------------------------------+
| TARGET: Individuals with P_s > 0.8 in Booth 04              |
| PSYCH FRAME: Loss Aversion (High Salience: Toll Road Fees)  |
+-------------------------------------------------------------+
| INTERVENTION PREVIEW:                                       |
| "Booth 04: Don't let your travel costs double. Vote..."     |
+-------------------------------------------------------------+
| [X] I certify this content matches the model's fairness gate. |
| [ APPROVE INTERVENTION ]  [ RE-CALIBRATE MATH MODEL ]        |
+-------------------------------------------------------------+
```

---

## 3. Visual Components for ML Team
*   **`st.pydeck_chart`**: Renders 3D bins using `avg_p_swing` from `mock_constituencies.csv`.
*   **`st.plotly_chart`**: Used to show histograms of individual `p_swing` scores within a selected booth.
*   **`st.metric`**: Displays the `fairness_metric` and `anomaly_score`.
