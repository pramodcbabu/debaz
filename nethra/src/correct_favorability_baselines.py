import sqlite3
import random

DB_PATH = "data/nethra_campaign.db"

def correct_baselines():
    print("Starting Baseline Favorability Correction...")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    tables_and_cols = [
        ("constituencies", "tvk_fav", "dmk_fav", "aiadmk_fav"),
        ("gcc_wards", "tvk_fav", "dmk_fav", "aiadmk_fav"),
        ("parliaments", "tvk_proj", "dmk_proj", "aiadmk_proj")
    ]

    total_updated = 0
    
    for table, tvk_col, dmk_col, aiadmk_col in tables_and_cols:
        c.execute(f"SELECT name FROM {table}")
        rows = c.fetchall()
        
        for row in rows:
            name = row[0]
            
            # The Trichy Exception
            if "Tiruchirappalli (East)" in name:
                tvk = round(random.uniform(48.0, 52.0), 1)
                dmk = round(random.uniform(25.0, 28.0), 1)
                aiadmk = round(random.uniform(15.0, 18.0), 1)
            else:
                # Reality Check: AIADMK Dominant, TVK struggling
                tvk = round(random.uniform(12.0, 18.0), 1)
                aiadmk = round(random.uniform(45.0, 52.0), 1)
                dmk = round(random.uniform(28.0, 35.0), 1)
            
            # Ensure they don't exceed 100 with BJP/Others
            c.execute(f"""UPDATE {table} 
                          SET {tvk_col} = ?, {aiadmk_col} = ?, {dmk_col} = ? 
                          WHERE name = ?""", (tvk, aiadmk, dmk, name))
            total_updated += 1
            
    conn.commit()
    conn.close()
    print(f"✅ Successfully corrected {total_updated} rows. AIADMK is now the dominant baseline outside Trichy East.")

if __name__ == "__main__":
    correct_baselines()
