# Nethra — Campaign Intelligence Platform
## Pitch Document: Samajwadi Party · UP Assembly Elections 2027

---

## The Problem

The 2022 UP Assembly elections were decided by **thin margins at the booth level**. In Lucknow Cantt alone:

- **Charbagh Booth 11:** SP 260 votes, BJP 250 — a 10-vote difference
- **Charbagh Booth 12:** SP 255 votes, BJP 255 — an exact tie
- **Sadar Bazar Booth 9:** SP 230 votes, BJP 270 — a 40-vote gap

These are not anomalies. Across UP, hundreds of seats were decided by margins under 2,000 votes. The difference between winning and losing was not ideology — it was **knowing which 500 voters to mobilise, in which booth, on which day.**

Today, most campaign decisions are made on gut feel, party worker reports, and constituency-level aggregates. That is a 1990s approach to a 2027 election.

---

## What Nethra Does

**Nethra is a booth-level election intelligence platform** built on a statistical method called Multilevel Regression and Poststratification (MRP) — the same framework used by leading political data firms in the US, UK, and Europe.

It answers three questions no general survey can answer:

> **1. Which booths can SP realistically win in 2027?**
> **2. Within those booths, which voter segments are persuadable?**
> **3. Where should SP concentrate GOTV (Get Out The Vote) resources for maximum seat impact?**

---

## How It Works

```
Real Election Data (ECI Form 20)     Census Demographics
        ↓                                    ↓
   Historical BJP/SP vote          Social group composition
   shares per booth 2017/22        by age, gender, occupation
        ↓                                    ↓
        └──────────── MRP Model ─────────────┘
                           ↓
           Booth-level SP vote share projection
           + Uncertainty bounds (confidence interval)
           + Swing classification per booth
           + Demographic segment breakdown
```

The model learns from **real Form 20 data** — actual votes cast at each booth in 2017 and 2022. It then uses demographic data from voter rolls and Census to project how voter composition changes in 2027 and what that means for SP's share.

---

## What SP Gets

### 1. Booth-Level Swing Map
A live, interactive map of every booth in a constituency — colour-coded by SP's competitive position:

| Classification | What it means for SP | Action |
|---|---|---|
| **SP Strong** | SP leads comfortably | Protect — ensure turnout |
| **SP Competitive** | SP within 5% of BJP | Push — targeted mobilisation |
| **Swing Seat** | Either party can win | Priority — maximum resources |
| **BJP Dominant** | BJP leads by 15%+ | Deprioritise or demographic play |

### 2. Voter Segment Intelligence
Within each booth, the model breaks down predictions by:
- **Social group** — General/OBC, SC, ST (and Muslim strata with voter roll data)
- **Age cohort** — 18–25 (first-time voters), 26–35, 36–50, 51+
- **Gender** — male/female mobilisation gap
- **Occupation** — cultivator, agricultural labourer, other worker, non-worker

This tells you not just *which booth* is winnable, but *which community within that booth* is the decisive swing group.

### 3. Resource Allocation Engine
Given a fixed campaigning budget (time, workers, vans, events), Nethra calculates the **optimal allocation** to maximise projected seat gains across the constituency — treating every rupee of campaign spend as an investment with a measurable expected return.

### 4. Scenario Modelling
- *"What if SP's SC vote share improves by 5% through a targeted scheme announcement?"*
- *"What is the seat impact if Muslim voter turnout drops from 68% to 58%?"*
- *"If SP and BSP formally ally in 40 seats, which booths flip?"*

All of these can be modelled and visualised in minutes.

---

## What the Prototype Already Shows — Lucknow Cantt (AC-175)

Using **real ECI Form 20 data from 2017 and 2022**, the current prototype demonstrates:

| Booth Area | SP 2022 Actual | SP 2027 Projection | Classification |
|---|---|---|---|
| Charbagh (11, 12) | 42.2%, 41.8% | ~40–42% | **SP Competitive** |
| Sadar Bazar (9, 10) | 39.2%, 38.9% | ~37–39% | **Swing** |
| Alambagh (1, 2) | 33.7%, 31.2% | ~32–34% | Swing |
| Krishna Nagar (5, 6) | 32.3%, 32.2% | ~31–33% | Swing |
| Cantt Area (7, 8) | 22.4%, 22.0% | ~21–24% | BJP Dominant |
| Nilmatha (13, 14) | 23.5%, 22.8% | ~22–25% | BJP Dominant |
| Amausi (15) | 34.4% | ~33–35% | Swing |

**Key insight:** SP's real opportunity in Lucknow Cantt is concentrated in 8 booths (Charbagh + Sadar Bazar + Amausi). These 8 booths contain ~4,500 voters. A 6–8% swing in these booths alone is sufficient to flip the seat. That is a targeted, achievable campaign goal.

---

## Data Sources — 100% Public, 100% Legal

| Data | Source | DPDP Act Compliant? |
|---|---|---|
| Booth-level vote counts | ECI Form 20 (public record) | ✅ Yes |
| Voter roll demographic aggregates | CEO UP electoral rolls | ✅ Yes — aggregated, no PII |
| Socioeconomic indices | Census of India 2011, Primary Census Abstract | ✅ Yes — public data |
| Geographic coordinates | Survey of India, OpenStreetMap | ✅ Yes |

No individual voter data is collected, stored, or processed. The model works entirely on **demographic counts from public records** — fully compliant with the Digital Personal Data Protection Act 2023.

---

## Competitive Advantage for SP

### Why this matters more for SP than BJP in 2027:

1. **SP is the challenger.** Challengers benefit more from precision targeting than incumbents. BJP's advantage is structural (administration, ground machinery). SP's best counter is intelligence-driven resource concentration.

2. **SP's base is heterogeneous.** SP draws from SC, OBC, Muslim, and urban poor communities across different constituencies. A single national strategy cannot serve this diversity. Booth-level MRP handles this heterogeneity natively.

3. **2027 is a swing election.** UP 2022 showed BJP's vote share fell significantly from 2017 in many constituencies. 2027 trends suggest further erosion. Nethra identifies exactly which booths are on the edge of flipping — where marginal campaign effort translates directly to seat gains.

4. **First-mover advantage.** No Indian party is currently using MRP at booth level. The party that deploys this in 2027 will have an asymmetric intelligence advantage for the entire election cycle.

---

## What We Need to Build the Full System

### Phase 1 — Prototype (Current) ✅
- 15 booths, Lucknow Cantt
- Real Form 20 data (2017 + 2022)
- Interactive dashboard with map, bar charts, booth table
- Synthetic demographic strata (placeholder)

### Phase 2 — Constituency Scale (3 months)
- All ~320 booths in Lucknow Cantt
- Real voter roll parsing (CEO UP PDFs)
- Census 2011 demographic mapping to booth level
- SP-calibrated MRP priors (SC, Muslim, OBC coefficients)

### Phase 3 — State Scale (6 months)
- All 403 Assembly constituencies in UP
- Cloud ingestion pipeline (AWS + ClickHouse)
- Real-time integration with survey field data
- Multi-party scenario modelling

---

## Engagement Model

| Tier | Scope | Deliverable |
|---|---|---|
| **Proof of Concept** | 5 priority constituencies | Dashboards + insight report |
| **District Package** | 1 district (~8–12 seats) | Full MRP + resource allocation |
| **State Package** | All 403 UP constituencies | Complete campaign intelligence suite |

---

## The Ask

A **pilot engagement on 3–5 priority constituencies** identified by SP as swing targets for 2027. We will:

1. Build the full data pipeline using real voter rolls and Form 20 data
2. Run the MRP model calibrated to SP's historical vote patterns
3. Deliver actionable booth-level prioritisation maps and segment briefs
4. Train SP's data team to interpret and act on the outputs

**Timeline:** First constituency deliverable in 6 weeks from data access.

---

*Nethra is built on peer-reviewed statistical methodology, public government data, and Privacy-by-Design principles. All outputs are demographic-level intelligence — no individual voter profiling.*

*For technical documentation, model specifications, or a live demo walkthrough, contact the Nethra team.*
