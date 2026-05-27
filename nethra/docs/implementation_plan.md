# Implementation Plan: Nethra Demographic Engine & Compliant Targeting API

This plan establishes the architecture and step-by-step roadmap for implementing Project **Nethra's** analytical core. It integrates the 2011 Census of India data, voter rolls, and behavioral psychological priors, and sets up a compliant ad-targeting payload bridge for Google and Meta.

---

## User Review Required

We have successfully resolved the key architectural branches of the design tree through our cooperative grill-me session. Please review and approve this technical blueprint.

> [!IMPORTANT]
> **Key Decisions Aligned:**
> 1. **Strata Integrity:** The poststratification frame will remain at **96 strata** (Gender [2] × Age [4] × Social Category [3] × Occupation [4]) to avoid sparse cells. Religion and detailed caste demographics will be integrated as village-level regression covariates, not direct strata dimensions.
> 2. **Dual-Track Target Payloads:** We bypass platform ad bans by using a bifurcated payload: precise PIN + Age + Gender on Google (with contextual placements), and broad district-level targeting on Meta (using hyper-local AI creative hooks to drive algorithmic self-selection).
> 3. **ECI MCMC Hard Lock:** Ad deployment is legally locked behind mandatory PDF upload and registration number inputs of the ECI Media Certification & Monitoring Committee approval.
> 4. **k-Anonymity Guardrail:** The data pipeline will automatically merge any demographic cell where $n_voters < 10$ to ensure 100% compliance with the **DPDP Act 2023**.

---

## Open Questions

There are no remaining blockages. Once you approve this plan, I will immediately scaffold the mathematical mock data and Streamlit UI coordinates for Track 1, and write the specifications for Track 2.

---

## Proposed Changes

We will group our file additions and modifications into the core layers: Data Crawling, Data/Model Engine, Strategy Documents, and Frontend UI.

### 0. Data Crawling & Ingestion (UP 2027)

To support the prototype development for the 2027 UP Assembly Elections, we will implement a dedicated data crawler and ingestion engine.

#### [NEW] [up_data_scraper.py](file:///Users/vinodh/debaz/nethra/src/up_data_scraper.py)
A multi-threaded Python scraping pipeline inside `src/`.
*   **Voter Roll PDF Scraper:** Crawls the Chief Electoral Officer (CEO) UP website (`ceouttarpradesh.nic.in`) to download assembly constituency voter roll PDFs. Employs a custom parsing script to extract age-gender counts per booth, securely discarding the PII immediately.
*   **ECI Form 20 Crawler:** Fetches historical booth-level election results (2017 & 2022 UP Legislative Assembly) from ECI and TCPD portals, parsing Excel/PDF files to construct the raw votes database.
*   **Census Table Downloader:** Downloads and extracts district-level UP Census 2011 Excel files (PCA, C-09 Education/Religion, B-04 economic, and HH-12 asset tables) directly from the ORGI portal.
*   **Geolocation Centroid Solver:** Geocodes polling station location address strings using OpenStreetMap/Nominatim to extract latitude/longitude centroids for spatial GIS overlays.

---

### 1. Model & Data Engineering Layer

#### [NEW] [poststratification_frame.csv](file:///Users/vinodh/debaz/nethra/data/poststratification_frame.csv)
The primary poststratification dataset mapped down to the booth and village level.
* Contains columns: `booth_id`, `age_group`, `gender`, `social_group`, `religion`, `education`, `occupation`, `n_voters`.

#### [NEW] [booth_covariates.csv](file:///Users/vinodh/debaz/nethra/data/booth_covariates.csv)
Booth-level socio-economic indicators, village directories, and ECI Form 20 past election stats.
* Contains columns: `booth_id`, `wealth_index`, `dilapidated_house_ratio`, `electricity_access_ratio`, `sanitation_deprivation_ratio`, `bank_distance_km`, `mobile_coverage_status`, `power_hours_domestic`, `historical_volatility_index`, `historical_margin_of_victory`.

#### [NEW] [mrp_engine.py](file:///Users/vinodh/debaz/nethra/src/mrp_engine.py)
The decoupled mathematical core.
* Implements the Bayesian hierarchical formulation with booth-level random effects ($\gamma_{booth}$) and poststratification scoring.
* Enforces the $k \ge 10$ anonymity boundary.

---

### 2. Strategy & Specification Layer

#### [MODIFY] [mathematical_model.md](file:///Users/vinodh/debaz/nethra/docs/mathematical_model.md)
Update to correct the obsolete micro-targeting targeting example and incorporate the raked census-bridge equations.

#### [MODIFY] [data_engineering.md](file:///Users/vinodh/debaz/nethra/docs/data_engineering.md)
Document the point-in-polygon spatial join workflow, raking mechanics, and the poststratification database schema.

---

### 3. Frontend & User Interface Layer

#### [NEW] [app.py](file:///Users/vinodh/debaz/nethra/app.py)
The Streamlit command center mockup interface.
* Renders PyDeck 3D maps displaying `volatility_index` and swing counts.
* Provides the demographic sensitivity audit tabs.
* Implements the Target Generator with the **MCMC Certificate Hard Lock** upload mechanism.
* Showcases both Meta and Google deployment payloads.

---

## Verification Plan

### Automated Verification
* Run unit tests on `mrp_engine.py` to ensure:
  1. The $k$-anonymity filter correctly merges cells under 10.
  2. The sum of projected swing votes matches the mathematical expectation $\sum N_k \cdot \hat{P}_k$.
* Execute Streamlit local test to verify PyDeck maps and Plotly distribution curves load without errors.

### Manual Verification
* Inspect the generated ad payloads in the UI to confirm that Meta never receives narrowed Age, Gender, or micro-locations, and Google never receives interest-based proxies.
* Verify that the "Deploy" button remains disabled until a dummy PDF is uploaded and a certification code is provided.
