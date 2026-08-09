import sqlite3
import pandas as pd
import random

DB_PATH = "data/nethra_campaign.db"
ASSEMBLY_CSV = "data/tn_assembly_234.csv"

def sync_baselines():
    print("Syncing Assembly Database baselines to CSV Ground Truth Vote Shares...")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    df_ac = pd.read_csv(ASSEMBLY_CSV)
    
    total_updated = 0
    for _, row in df_ac.iterrows():
        name = row['name']
        
        # Multiply actual vote share by 100 to get exact favorability
        tvk_fav = round(float(row['tvk_share_2026']) * 100, 1)
        dmk_fav = round(float(row['dmk_share_2026']) * 100, 1)
        aiadmk_fav = round(float(row['aiadmk_share_2026']) * 100, 1)
        
        c.execute("""
            UPDATE constituencies 
            SET tvk_fav = ?, dmk_fav = ?, aiadmk_fav = ?
            WHERE name = ?
        """, (tvk_fav, dmk_fav, aiadmk_fav, name))
        
        total_updated += 1
        
    conn.commit()
    conn.close()
    print(f"✅ Successfully synced {total_updated} assembly constituencies with exact ground-truth 2026 vote shares.")

if __name__ == "__main__":
    sync_baselines()
