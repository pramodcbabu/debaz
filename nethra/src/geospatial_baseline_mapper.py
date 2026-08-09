import pandas as pd
import math

def haversine(lat1, lon1, lat2, lon2):
    # Calculate distance between two lat/lon points in km
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def get_closest_assembly_averages(target_lat, target_lon, df_ac, k=3):
    distances = []
    for idx, row in df_ac.iterrows():
        dist = haversine(target_lat, target_lon, row['lat'], row['lon'])
        distances.append((dist, row))
        
    distances.sort(key=lambda x: x[0])
    closest = distances[:k]
    
    tvk_sum, dmk_sum, aiadmk_sum = 0, 0, 0
    for dist, row in closest:
        tvk_sum += float(row['tvk_share_actual'])
        dmk_sum += float(row['dmk_share_actual'])
        aiadmk_sum += float(row['aiadmk_share_actual'])
        
    return round(tvk_sum/k, 3), round(dmk_sum/k, 3), round(aiadmk_sum/k, 3)

if __name__ == "__main__":
    print("Loading datasets...")
    df_ac = pd.read_csv("data/tn_assembly_234.csv")
    df_gcc = pd.read_csv("data/tn_chennai_wards_200.csv")
    df_pc = pd.read_csv("data/tn_parliament_39.csv")
    
    print("Mapping GCC Wards (200) to closest Assembly Constituencies...")
    for idx, row in df_gcc.iterrows():
        tvk_est, dmk_est, aiadmk_est = get_closest_assembly_averages(row['lat'], row['lon'], df_ac, k=3)
        df_gcc.at[idx, 'tvk_share_actual'] = tvk_est
        df_gcc.at[idx, 'dmk_share_actual'] = dmk_est
        df_gcc.at[idx, 'aiadmk_share_actual'] = aiadmk_est
        
        df_gcc.at[idx, 'tvk_fav'] = round(tvk_est * 100, 1)  # Initialize live target to estimated baseline
        df_gcc.at[idx, 'dmk_fav'] = round(dmk_est * 100, 1)
        df_gcc.at[idx, 'aiadmk_fav'] = round(aiadmk_est * 100, 1)
        
        # Ensure winner is accurate
        parties = {"DMK": dmk_est, "AIADMK": aiadmk_est, "TVK": tvk_est}
        winner = max(parties, key=parties.get)
        df_gcc.at[idx, 'winner_actual'] = winner
        
    df_gcc.to_csv("data/tn_chennai_wards_200.csv", index=False)
    print("✅ Mapped GCC Wards.")

    print("Mapping Lok Sabha (39) to closest Assembly Constituencies...")
    for idx, row in df_pc.iterrows():
        # Lok Sabha seats encompass ~6 assembly seats, so average 6 closest!
        tvk_est, dmk_est, aiadmk_est = get_closest_assembly_averages(row['lat'], row['lon'], df_ac, k=6)
        df_pc.at[idx, 'tvk_share_actual'] = tvk_est
        df_pc.at[idx, 'dmk_share_actual'] = dmk_est
        df_pc.at[idx, 'aiadmk_share_actual'] = aiadmk_est
        
        if 'tvk_proj' in df_pc.columns:
            df_pc.at[idx, 'tvk_proj'] = round(tvk_est * 100, 1)
            df_pc.at[idx, 'dmk_proj'] = round(dmk_est * 100, 1)
            df_pc.at[idx, 'aiadmk_proj'] = round(aiadmk_est * 100, 1)
            
        df_pc.at[idx, 'tvk_fav'] = round(tvk_est * 100, 1)
        df_pc.at[idx, 'dmk_fav'] = round(dmk_est * 100, 1)
        df_pc.at[idx, 'aiadmk_fav'] = round(aiadmk_est * 100, 1)
        
        parties = {"DMK": dmk_est, "AIADMK": aiadmk_est, "TVK": tvk_est}
        winner = max(parties, key=parties.get)
        df_pc.at[idx, 'winner_actual'] = winner
        
    df_pc.to_csv("data/tn_parliament_39.csv", index=False)
    print("✅ Mapped Lok Sabha Parliaments.")
