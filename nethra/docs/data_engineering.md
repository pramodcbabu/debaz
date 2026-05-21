# Data Engineering & Privacy Strategy

## 1. Prototype Strategy: Mock Data First
To ensure a rapid BD cycle, we will generate a high-fidelity CSV file (`mock_constituencies.csv`) that simulates the output of our production pipeline.

### `mock_constituencies.csv` Schema (Transformed Layer)
| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | STRING | Unique Booth/Constituency ID |
| `lat` / `lon` | FLOAT | Geographic coordinates for PyDeck mapping |
| `swing_voter_pct` | FLOAT | 0.0 - 1.0 (Powers the heatmap) |
| `top_issue_1` | STRING | Local grievance (e.g., "Toll Road Prices") |
| `recommended_frame`| STRING | e.g., "Loss Aversion", "Community Pride" |
| `cadre_report_val` | FLOAT | The "fake" report from ground workers |
| `historical_baseline`| FLOAT | The true historical vote share (ECI) |
| `approval_status` | BOOLEAN| HITL flag (Default: False) |
| `hashed_voter_list` | JSON | Simulated list of SHA-256 hashed phone numbers |

---

## 2. Production Data Sources (The Ingestion Layer)
For the **IT Cell Pitch**, we highlight the diversity of our data sources:

1.  **ECI Public Data:** Historical Form 20 (Booth-level results) parsed via Python OCR/PDF scrapers.
2.  **Cadre Ground Data:** Direct API ingestion from internal apps like **SARAL** or **Shakti** (provides raw PII).
3.  **Social Listening:** Scraping public Social Media APIs (X, Meta, YouTube) for keyword saliency in regional dialects.

### Raw Schema Example: `voter_ground_reports`
```json
{
  "booth_id": "AC-125-B04",
  "voter_name": "Rajesh Kumar",
  "phone_number": "+91-9876543210", 
  "disposition": "Undecided",
  "primary_concern": "Water Supply",
  "timestamp": "2026-05-15T10:30:00Z"
}
```

---

## 3. The Privacy Pipeline (SHA-256 Hashing)
To satisfy the **Political Party's** security requirements and comply with the **DPDP Act**, we use a one-way hashing pipeline.

### Data Flow (ML Perspective)
1.  **Raw Ingestion:** PII is ingested into a transient, encrypted memory buffer.
2.  **Hashing Function:**
    ```python
    import hashlib
    
    def hash_pii(phone, salt="nethra_2026"):
        return hashlib.sha256((phone + salt).encode()).hexdigest()
    ```
3.  **Outcome:** The raw phone number is purged. Only the `hashed_pii` is stored in the analytics database and uploaded to ad platforms.

### Example: Simulated Prototype Output
```csv
id,lat,lon,swing_voter_pct,top_issue_1,hashed_voter_list
B01,13.08,80.27,0.45,"Youth Jobs","['ef92...','3a4b...']"
B02,13.09,80.28,0.12,"Water Supply","['c8d1...','7f6e...']"
```

---

## 4. Data Sovereignty Mandate
*   **Ownership:** All hashed datasets reside in the Party's own cloud environment.
*   **Shredding:** Automated lifecycle hooks cryptographically shred all temporary PII buffers 7 days post-election.
