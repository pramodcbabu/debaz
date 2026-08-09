import pandas as pd

CSV_PATH = "data/tn_assembly_234.csv"

def inject_truth():
    print(f"Reading uncorrupted {CSV_PATH}...")
    df = pd.read_csv(CSV_PATH)
    
    # 1. Apply Canonical Target Overrides
    overrides = {
        "Karur": {"winner": "AIADMK", "tvk": 0.35, "dmk": 0.20, "aiadmk": 0.45},
        "Perundurai": {"winner": "AIADMK", "tvk": 0.38, "dmk": 0.14, "aiadmk": 0.48},
        "Viralimalai": {"winner": "AIADMK", "tvk": 0.36, "dmk": 0.18, "aiadmk": 0.46},
        "Ambasamudram": {"winner": "AIADMK", "tvk": 0.34, "dmk": 0.22, "aiadmk": 0.44},
        "Tiruchirappalli (East)": {"winner": "TVK", "tvk": 0.49, "dmk": 0.39, "aiadmk": 0.12},
    }
    
    for unit, data in overrides.items():
        idx = df.index[df['name'] == unit]
        if not idx.empty:
            i = idx[0]
            df.at[i, 'winner_2026'] = data['winner']
            df.at[i, 'tvk_share_2026'] = data['tvk']
            df.at[i, 'dmk_share_2026'] = data['dmk']
            df.at[i, 'aiadmk_share_2026'] = data['aiadmk']
            
            # Recalculate margins based on override
            parties = {"TVK": data['tvk'], "DMK": data['dmk'], "AIADMK": data['aiadmk']}
            sorted_parties = sorted(parties.items(), key=lambda item: item[1], reverse=True)
            winner_share = sorted_parties[0][1]
            runner_share = sorted_parties[1][1]
            lead = round((winner_share - runner_share) * 100.0, 1)
            
            if data['winner'] == "TVK":
                df.at[i, 'tvk_lead'] = lead
            else:
                df.at[i, 'tvk_lead'] = round((data['tvk'] - winner_share) * 100.0, 1)
                
            print(f"Applied Canonical Override to {unit}: {data['winner']} wins.")
            
    # 2. Lock the Baseline (Set all _fav columns to strictly equal _share_2026 * 100)
    for idx, row in df.iterrows():
        tvk_s = float(row.get('tvk_share_2026', 0))
        dmk_s = float(row.get('dmk_share_2026', 0))
        adk_s = float(row.get('aiadmk_share_2026', 0))
        
        df.at[idx, 'tvk_fav'] = round(tvk_s * 100.0, 1)
        df.at[idx, 'dmk_fav'] = round(dmk_s * 100.0, 1)
        df.at[idx, 'aiadmk_fav'] = round(adk_s * 100.0, 1)
        
        # We also need to fix tvk_lead for ALL other columns just to be safe
        parties = {"TVK": tvk_s, "DMK": dmk_s, "AIADMK": adk_s}
        sorted_parties = sorted(parties.items(), key=lambda item: item[1], reverse=True)
        winner_share = sorted_parties[0][1]
        runner_share = sorted_parties[1][1]
        
        # Don't change winner_2026 for others (keep original CSV truth)
        winner_2026 = str(row['winner_2026']).upper()
        if winner_2026 == "TVK":
            df.at[idx, 'tvk_lead'] = round((winner_share - runner_share) * 100.0, 1)
        else:
            df.at[idx, 'tvk_lead'] = round((tvk_s - winner_share) * 100.0, 1)

    df.to_csv(CSV_PATH, index=False)
    print(f"✅ Successfully locked true baseline across all 234 seats in {CSV_PATH}.")

if __name__ == "__main__":
    inject_truth()
