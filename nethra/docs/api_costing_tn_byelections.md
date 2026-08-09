# API & AI Costing Projections: TN Byelections (Frontier Models)

## Executive Summary
This document provides a detailed commercial projection for monitoring strategic social media accounts, evaluating the content for authenticity, geo-relevance, and issue-mapping, and automatically generating hyper-local campaign content over a 30-day active campaign window for the Tamil Nadu assembly byelections. This projection specifically factors in the use of high-fidelity "Frontier AI" models for maximum nuance.

## 1. Operating Assumptions
- **Target Volume:** 100,000 posts per month.
- **Campaign Duration:** 30 days of active mining.
- **Verification Yield:** We assume roughly 20% of the posts (20,000) will be highly relevant and require AI campaign message generation.
- **AI Pricing:** Utilizing Frontier AI models (e.g., GPT-4 class or Gemini 1.5 Pro equivalents) at an estimated flat rate of **$20.00 per 1 Million Tokens** (blended/average input and output).

---

## 2. Platform API Scraping Costs (Data Ingestion)
Since native platform APIs are heavily gated or strictly metered, we rely on authenticated Data Broker APIs (e.g., Apify, TwitterAPI.io, or Official Enterprise tiers) to guarantee zero downtime.

| Platform / Source | Expected Volume | Cost per 1,000 Posts | Estimated Monthly Cost (USD) | Estimated Monthly Cost (INR) |
| :--- | :--- | :--- | :--- | :--- |
| **X (Twitter)** | 60,000 posts | $5.00 (Official API scale) | $300.00 | ₹25,200 |
| **Meta (FB/IG)** | 30,000 posts | $2.00 (Apify Scrapers) | $60.00 | ₹5,040 |
| **YouTube** | 10,000 posts | Free (Data API Quota) | $0.00 | ₹0 |
| **Subtotal** | **100,000 posts** | - | **$360.00** | **₹30,240** |

---

## 3. AI Processing Costs (Frontier Models @ $20/M Tokens)
All incoming posts must pass through a strict verification gate before being used to generate campaign material. Because we are using frontier models, the nuance will be exceptionally high, but costs scale proportionately.

### Phase A: Content Verification & Scoring
Each of the 100,000 posts is run against the frontier AI to assess **Authenticity** and **Geo-Relevance**.
- **Input Tokens per post:** ~500 tokens (System prompt, issue constraints, raw post text/URL)
- **Output Tokens per post:** ~100 tokens (JSON output with reasoning and scores)
- **Total Input Tokens:** `100,000 × 500 = 50.0 Million Tokens`
- **Total Output Tokens:** `100,000 × 100 = 10.0 Million Tokens`
- **Total Combined Tokens:** 60.0 Million Tokens
- **Verification Subtotal:** `60.0M × $20.00 / 1M` = **$1,200.00 (₹1,00,800)**

### Phase B: Campaign Content Generation
For the estimated 20,000 highly verified posts, the AI generates localized campaign assets (Tamil WhatsApp forward, Tamil Instagram caption, English X post).
- **Input Tokens per post:** ~400 tokens (Verified context + Generation guidelines)
- **Output Tokens per post:** ~300 tokens (3 distinct social media texts + hashtags)
- **Total Input Tokens:** `20,000 × 400 = 8.0 Million Tokens`
- **Total Output Tokens:** `20,000 × 300 = 6.0 Million Tokens`
- **Total Combined Tokens:** 14.0 Million Tokens
- **Generation Subtotal:** `14.0M × $20.00 / 1M` = **$280.00 (₹23,520)**

---

## 4. Total Monthly Infrastructure Projections

| Service Segment | Estimated Monthly Cost (USD) | Estimated Monthly Cost (INR) |
| :--- | :--- | :--- |
| **Data Ingestion (Platform APIs)** | $360.00 | ₹30,240 |
| **AI Verification (Frontier AI)** | $1,200.00 | ₹1,00,800 |
| **AI Content Generation (Frontier AI)** | $280.00 | ₹23,520 |
| **Server/Compute & DB Hosting** | $30.00 | ₹2,520 |
| **Total Estimated Run-Rate** | **~$1,870.00** | **~₹1,57,080** |

## Conclusion
Migrating to a Frontier AI model for 100,000 monthly posts provides a significantly higher quality of political nuance and analytical accuracy. This raises the AI processing overhead from nominal figures (in cheaper models) to approximately **$1,480 per month**. Combined with the $360 in data ingestion infrastructure, the total monthly budget scales gracefully to roughly $1,870 for enterprise-grade campaign intelligence.
