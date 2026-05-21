# Nethra: The Mathematical Foundation

## 1. The Booth Volatility Index (BVI)
The BVI is a composite score (0 to 1.0) calculated for every polling booth.

$$ BVI = \alpha \cdot M_{hist} + \beta \cdot S_{vol} + \gamma \cdot I_{unrest} $$

- **$M_{hist}$ (Historical Margin):** Normalized historical victory margin.
- **$S_{vol}$ (Sentiment Volatility):** Variance in sentiment over a 30-day window from AI surveys.
- **$I_{unrest}$ (Issue Unrest):** Density of specific local grievances compared to regional averages.

```mermaid
graph TD
    subgraph Inputs
        A[ECI Historical Margin]
        B[Survey Sentiment Volatility]
        C[NLP Issue Density]
    end
    
    subgraph Processing
        A --> D[Weighting Engine]
        B --> D
        C --> D
        D --> E[Dirty Data Filter / Anomaly Detection]
    end
    
    subgraph Output
        E --> F[Booth Volatility Index]
        F --> G[Ranked Swing Voter Target List]
    end
```

## 2. The "Dirty Data" Anomaly Detection
Nethra uses a Cross-Validation Model to penalize cadre data that significantly deviates from AI survey engine ground-truth.

## 3. Causal Inference & ROI Verification
To prove ROI, Nethra employs a **Control vs. Treatment** methodology at the booth level.

```mermaid
graph LR
    subgraph Experiment Design
        A[Identify 100 Volatile Booths]
        A --> B[Random Assignment]
        B --> C[Treatment Group: 50 Booths]
        B --> D[Control Group: 50 Booths]
    end
    
    subgraph Intervention
        C --> E[Nethra Active: Targeted Ads + AI Interventions]
        D --> F[Status Quo: Traditional Campaigning Only]
    end
    
    subgraph Measurement
        E --> G[Vote Day Results]
        F --> G
        G --> H[Calculate Average Treatment Effect - ATE]
    end
```

$$ ATE = E[Y_1 - Y_0] $$

## 4. Swing Voter Clustering
Using K-Means clustering on multidimensional sentiment vectors to identify the "Psychological Profile" of the swing voter for content generation.
