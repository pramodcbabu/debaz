import sqlite3
import pandas as pd

DB_PATH = "data/nethra_campaign.db"

def sync_baselines():
    print("Syncing Universal Baselines to nethra_campaign.db...")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    datasets = [
        ("data/tn_assembly_234.csv", "constituencies"),
        ("data/tn_chennai_wards_200.csv", "gcc_wards"),
        ("data/tn_parliament_39.csv", "parliaments")
    ]
    
    for csv_file, table_name in datasets:
        df = pd.read_csv(csv_file)
        total_updated = 0
        for _, row in df.iterrows():
            name = row['name']
            
            # Universal actuals
            tvk_fav = round(float(row.get('tvk_share_actual', 0.15)) * 100, 1)
            dmk_fav = round(float(row.get('dmk_share_actual', 0.40)) * 100, 1)
            aiadmk_fav = round(float(row.get('aiadmk_share_actual', 0.45)) * 100, 1)
            
            if table_name == "parliaments":
                c.execute(f"UPDATE {table_name} SET tvk_proj = ?, dmk_proj = ?, aiadmk_proj = ? WHERE name = ?", (tvk_fav, dmk_fav, aiadmk_fav, name))
            else:
                c.execute(f"UPDATE {table_name} SET tvk_fav = ?, dmk_fav = ?, aiadmk_fav = ? WHERE name = ?", (tvk_fav, dmk_fav, aiadmk_fav, name))
            
            total_updated += 1
            
        print(f"✅ Synced {total_updated} rows in {table_name}.")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    sync_baselines()
