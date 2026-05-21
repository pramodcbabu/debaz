# Nethra Command Center: Visualization Specs

## 1. Dashboard User Flow
```mermaid
graph LR
    A[State/District Map View] --> B[Booth Volatility Heatmap]
    B --> C{Select Volatile Booth}
    C --> D[Issue & Sentiment Deep-Dive]
    D --> E[Simulated Anomaly Check]
    E --> F[Audience Size: 240 Swing Voters]
    F --> G[Intervention: Dispatch AI Ad Campaign]
    G --> H[Real-time ROI Monitoring]
```

## 2. The "Booth Intelligence" UI Component
**BOOTH: TN-234-001 (Tiruchi East)**
- **Volatility Index:** 0.88 (CRITICAL)
- **Top Grievances:** Youth Unemployment, Irregular Water Supply.
- **Cadre Status:** ANOMALY DETECTED.

## 3. Visual Design Standards
- **Theme:** Dark Mode primary.
- **Geospatial:** MapBox GL JS for booth-level zooming.
- **Sentiment Indicators:** Green (+1.0) supporters, Red (-1.0) angry opponents, Yellow (0) swing voters.
