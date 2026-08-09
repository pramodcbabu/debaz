import pandas as pd

CSV_PATH = "data/tn_assembly_234.csv"

def rebuild_csv():
    print(f"Reading {CSV_PATH}...")
    df = pd.read_csv(CSV_PATH)
    
    total_updated = 0
    for idx, row in df.iterrows():
        # Get the true favorabilities
        tvk_fav = float(row.get('tvk_fav', 0))
        dmk_fav = float(row.get('dmk_fav', 0))
        aiadmk_fav = float(row.get('aiadmk_fav', 0))
        
        # Recalculate true share
        true_tvk_share = round(tvk_fav / 100.0, 3)
        true_dmk_share = round(dmk_fav / 100.0, 3)
        true_aiadmk_share = round(aiadmk_fav / 100.0, 3)
        
        df.at[idx, 'tvk_share_2026'] = true_tvk_share
        df.at[idx, 'dmk_share_2026'] = true_dmk_share
        df.at[idx, 'aiadmk_share_2026'] = true_aiadmk_share
        
        # Calculate winner
        parties = {"TVK": true_tvk_share, "DMK": true_dmk_share, "AIADMK": true_aiadmk_share}
        sorted_parties = sorted(parties.items(), key=lambda item: item[1], reverse=True)
        
        winner_party = sorted_parties[0][0]
        runner_party = sorted_parties[1][0]
        winner_share = sorted_parties[0][1]
        runner_share = sorted_parties[1][1]
        
        df.at[idx, 'winner_2026'] = winner_party
        
        # Lead margin
        lead = round((winner_share - runner_share) * 100.0, 1)
        if winner_party == "TVK":
            df.at[idx, 'tvk_lead'] = lead
        else:
            df.at[idx, 'tvk_lead'] = round((true_tvk_share - winner_share) * 100.0, 1)
            
        total_updated += 1
        
    df.to_csv(CSV_PATH, index=False)
    print(f"✅ Successfully recalculated {total_updated} rows in {CSV_PATH}.")

if __name__ == "__main__":
    rebuild_csv()
