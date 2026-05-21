# Nethra Command Center: Visualization Specs

## 1. Dashboard Architecture
- **Tech Stack:** Next.js, `shadcn/ui`, `Zustand` (State), `Mapbox GL JS` with `Deck.gl` (Geospatial rendering).
- **Communication:** WebSockets for real-time booth updates during polling day.

## 2. Dual-Mode Interface
### 2.1 Executive Summary View (Political Leadership)
- **Opportunity Heatmap:** District-level map using **Hex-bins** (size = volatility, color = sentiment).
- **Actionable Metrics:** "Swing Budget Efficiency", "Top 3 District Risks", "Daily Swung Vote Est."
- **1-Click Briefing Export:** Automated generation of a "Morning Briefing" PDF summarizing key shifts in the last 24 hours for leadership meetings.

### 2.2 Data Science Deep-Dive (IT/Analytical Team)
- **Model Health:** Drift metrics for the BVI model.
- **Anomaly Logs:** Detailed view of flagged cadre reports with "Reasoning" (e.g., "Deviation from Survey Sentiment by >3 sigma").
- **Match Rate Dashboard:** Current match rates on Meta (Facebook/IG) and Google (YT).

## 3. The Geospatial "Booth Intel" Widget
**BOOTH: TN-234-001 (Tiruchi East)**
- **Executive View:** 
    - Opportunity: 8.8 (HIGH)
    - Est. Swing Votes: 240
    - Top Grievance: Youth Unemployment
- **DS View (Toggle):** 
    - BVI Breakdown: [$M$: 0.2, $S$: 0.8, $I$: 0.6]
    - Match Rate: Meta (72%), Google (68%)
    - Cluster Type: "Aspirational Middle Class"

## 4. Compliance & Safety Hub
- **Silent Period Kill Switch:** Persistent, global red button in the header. Activating it kills all worker processes and pauses all ad-tech API sessions instantly.
- **Audit Logs:** Immutable log of every hashed phone number exported to Meta/Google, timestamped and attributed to a user ID.
- **Role-Based Access (RBAC):**
    - **Level 1 (Central):** Global view, campaign dispatch.
    - **Level 2 (District):** District view, no dispatch.
    - **Level 3 (Observer):** View-only aggregated data.
