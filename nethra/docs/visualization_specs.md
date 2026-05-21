# Nethra Command Center: Visualization Specs

## 1. Prototype UI Strategy (Speed & Impact)
The prototype UI must be highly polished visually but technically simple. It acts as a "clickable mockup" built using **Streamlit**.

*   **Tech Stack:** Streamlit (Frontend), PyDeck (Geospatial Mapping), Pandas (Data Handling).
*   **Visual Standards:** Dark Mode primary for a "War Room" aesthetic. High-contrast colors for volatility/opportunity scores.

## 2. The Core Demo Script (User Flow)
The salesperson will walk the political client through this exact flow:

### Step 1: The Macro View (The Map)
- **Visual:** A Mapbox-powered hex-bin map of a simulated district.
- **Narrative:** "Here is your district. The purple and red areas indicate the highest concentration of **Swing Voters**—the people who will actually decide the election."

### Step 2: The Deep-Dive (Constituency Intel)
- **Visual:** The user clicks a hex-bin. A sidebar populates with metrics.
- **Metrics:** 
    - **Opportunity Score:** 8.8 (High Priority)
    - **Swing Population:** 14,200 Voters
    - **Key Issues:** Youth Unemployment, Water Supply.
- **Narrative:** "In this specific booth, your biggest problem isn't the opposition—it's that 14,000 people are undecided because of local water issues. Your cadre is reporting 90% support, but the AI detects a massive **Anomaly** based on historical baseline."

### Step 3: The Intervention (The Generator)
- **Visual:** Clicking a "Generate Engagement" button. A loading spinner appears, then the **Gemini API** outputs a tailored campaign.
- **Output:** 
    - **Campaign Type:** Instagram Reel / WhatsApp Forward.
    - **Targeting:** Unemployed Gen-Z voters in Booth X.
    - **The Script:** A punchy, localized 15-second script addressing the specific water grievance and the party's solution.
- **Narrative:** "With one click, we've moved from data to action. Your IT cell can now deploy this exact script to influence that specific population tonight."

## 3. Visual Components
- **`st.pydeck_chart`**: For the interactive 3D hex-bin map.
- **`st.metric`**: For high-impact numbers (Swing population, Opportunity score).
- **`st.expander`**: For the "Data Science" view showing the anomaly detection logic.
- **`st.write_stream`**: To show the AI-generated ad script "typing out" in real-time for dramatic effect.

## 4. Production Features (Post-Contract)
- **Real-time Streaming:** Seeing sentiment shifts live during a rally.
- **Silent Period Kill Switch:** A global red button in the header.
- **Morning Briefing Export:** 1-click PDF summary for the leader's tablet.
