# src/data_crawler.py
"""High‑level data ingestion wrapper for the Nethra prototype.
It simply invokes the full ingestion pipeline defined in
`up_data_scraper.py` (which handles voter rolls, Form 20, census
and geocoding) and stores the resulting CSVs under `data/`.
"""

import sys
from pathlib import Path

# Ensure the project root is on the path for relative imports
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.up_data_scraper import run_ingestion_pipeline

def main(mock: bool = True, output_dir: str = "data") -> bool:
    """Execute the full ingestion pipeline.

    Parameters
    ----------
    mock: bool
        When True, all network operations are simulated (default).
    output_dir: str
        Directory where the generated CSV files will be placed.
    """
    return run_ingestion_pipeline(mock=mock, output_dir=output_dir)

if __name__ == "__main__":
    # Simple CLI for manual runs
    import argparse
    parser = argparse.ArgumentParser(description="Run Nethra data crawler")
    parser.add_argument("--real", action="store_true", help="Disable mock mode and fetch real data")
    parser.add_argument("--out", default="data", help="Output directory")
    args = parser.parse_args()
    success = main(mock=not args.real, output_dir=args.out)
    print("Ingestion pipeline completed:" , success)
