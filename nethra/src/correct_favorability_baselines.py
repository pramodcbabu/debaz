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
        if table == "parliaments":
            c.execute(f"SELECT name, region FROM {table}")
        else:
            c.execute(f"SELECT name, region FROM {table}")
        rows = c.fetchall()
        
        for row in rows:
            name = row[0]
            
            # Region Logic
            # Chennai & North (DMK Stronghold)
            if any(dist in name or dist in str(row[1]) for dist in ["Chennai", "Tiruvallur", "Kanchipuram", "Chengalpattu", "Vellore", "Ranipet", "Tirupathur", "Tiruvannamalai", "Villupuram", "Kallakurichi"]):
                dmk = round(random.uniform(40.0, 50.0), 1)
                aiadmk = round(random.uniform(20.0, 30.0), 1)
                tvk = round(random.uniform(15.0, 25.0), 1)
            # Kongu Belt & West (AIADMK Stronghold)
            elif any(dist in name or dist in str(row[1]) for dist in ["Coimbatore", "Tiruppur", "Erode", "Salem", "Namakkal", "Karur", "Nilgiris", "Dharmapuri", "Krishnagiri"]):
                aiadmk = round(random.uniform(42.0, 52.0), 1)
                dmk = round(random.uniform(20.0, 30.0), 1)
                tvk = round(random.uniform(15.0, 25.0), 1)
            # South & Delta (TVK / DMK Battleground)
            else:
                tvk = round(random.uniform(38.0, 48.0), 1)
                dmk = round(random.uniform(35.0, 40.0), 1)
                aiadmk = round(random.uniform(10.0, 18.0), 1)
            
            # The 5 Target Exceptions
            if "Tiruchirappalli (East)" in name:
                tvk = round(random.uniform(48.0, 52.0), 1); dmk = 25.0; aiadmk = 15.0
            elif "Karur" in name:
                aiadmk = round(random.uniform(45.0, 49.0), 1); dmk = 25.0; tvk = 20.0
            elif "Perundurai" in name:
                aiadmk = round(random.uniform(48.0, 52.0), 1); dmk = 22.0; tvk = 18.0
            elif "Viralimalai" in name:
                dmk = round(random.uniform(40.0, 45.0), 1); aiadmk = 35.0; tvk = 15.0
            elif "Ambasamudram" in name:
                tvk = round(random.uniform(40.0, 45.0), 1); aiadmk = 35.0; dmk = 15.0
                
            c.execute(f"""UPDATE {table} 
                          SET {tvk_col} = ?, {aiadmk_col} = ?, {dmk_col} = ? 
                          WHERE name = ?""", (tvk, aiadmk, dmk, name))
            total_updated += 1
            
    conn.commit()
    conn.close()
    print(f"✅ Successfully corrected {total_updated} rows. Realistic Regional Mandates applied.")

if __name__ == "__main__":
    correct_baselines()
