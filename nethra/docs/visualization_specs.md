# Nethra Command Center: Visualization Specs

## 1. Prototype UI Strategy (The War Room Aesthetic)
The prototype UI acts as a "clickable mockup" designed to impress **Political Leadership** while providing structured targets for the **ML/Data Engineering** team.

*   **Tech Stack:** Streamlit (Frontend), PyDeck (Geospatial Mapping), Pandas (Data Handling).
*   **Aesthetic:** Dark Mode primary, high-contrast markers for "Swing Density," and clean metric cards for ROI-focused KPIs.

---

## 2. Visual Mockups (ASCII Wireframes)

### Mockup 1: The Macro View (District Map)
*Goal: Provide a high-level overview of volatility across the district.*

```text
+-------------------------------------------------------------+
| NETHRA COMMAND CENTER | [Red Button] SILENT PERIOD KILL SWITCH |
+-------------------------------------------------------------+
|                                                             |
|   [ HEX-BIN MAP OF DISTRICT ]                               |
|   (Color gradient from Dark Blue to Neon Pink)              |
|   Neon Pink = High Swing Density (Action Required)          |
|                                                             |
+-------------------------------------------------------------+
| DISTRICT STATS:                                             |
| [ Total Swing Pop: 142k ] [ Avg Opportunity: 7.2 ]          |
+-------------------------------------------------------------+
```

### Mockup 2: The Deep-Dive (Constituency Sidebar)
*Goal: Display actionable intelligence for a selected booth.*

```text
+-----------------------+---------------------------------------+
|  BOOTH INTELLIGENCE   | SELECTED: AC-125 BOOTH 04             |
+-----------------------+---------------------------------------+
| Swing Density: 88%    | TOP ISSUES:                           |
| Total Volatile: 1,400 | 1. [YOUTH JOBS]     (Salience: 0.9)   |
| Opportunity Score: 9.1| 2. [TOLL ROAD FEES] (Salience: 0.7)   |
+-----------------------+---------------------------------------+
| [!] ANOMALY DETECTED:                                         |
| Cadre reports 95% support, but historical baseline is 40%.    |
| Probability of Cadre Inflation: HIGH                          |
+-----------------------+---------------------------------------+
```

### Mockup 3: The Intervention (The Generator)
*Goal: Demonstrate the transition from data to ethically-vetted, psychologically-resonant action.*

```text
+-------------------------------------------------------------+
| [ GENERATE SOCIAL MEDIA CAMPAIGN ]                          |
+-------------------------------------------------------------+
| TARGET: Gen-Z Swing Voters in Booth 04                      |
| THEME: Local Job Growth vs Opposition Record                |
| PSYCH FRAME: [x] Loss Aversion [ ] Community Pride          |
+-------------------------------------------------------------+
| CAMPAIGN SCRIPT (AI GENERATED):                             |
| "Namaste Booth 04! Fed up of the toll prices and no jobs?   |
| [Candidate Name] has a plan for the local IT park..."       |
+-------------------------------------------------------------+
| [X] I certify this content contains NO DEEPFAKES.           |
| [ APPROVE & SEND TO META ]  [ REGENERATE ] [ EXPORT ]       |
+-------------------------------------------------------------+
```

---

## 3. Core Interaction Flow (The Demo Script)
The salesperson will walk the political client through this exact flow:

1.  **Macro-Awareness:** "Behold your district. The pink zones are where the election will be won or lost tonight."
2.  **Granular Intel:** "Look at Booth 04. Your cadre says everything is fine, but our AI sees a massive volatility spike due to toll road prices. 1,400 voters are in play."
3.  **Instant Intervention:** "We don't just report—we act. With one click, we've generated a tailored script for that specific booth, ready for Instagram Reels."

---

## 4. Visual Components for ML Team
*   **`st.pydeck_chart`**: Renders the 3D hex-bins using `swing_voter_pct` from `mock_constituencies.csv`.
*   **`st.metric`**: Used for high-impact numbers (Opportunity score, Volatile population).
*   **`st.write_stream`**: Shows the AI script "typing out" in real-time, simulating live LLM generation.
