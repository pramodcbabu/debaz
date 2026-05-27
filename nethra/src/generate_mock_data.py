import os
import csv
import random

def generate_data():
    print("--- Generating Poststratification Frame & Booth Covariates for Nethra UP 2027 ---")
    
    # Booth sizes matching 2022 electorate counts from UP Form 20 sample
    booths = [
        {"id": 1, "name": "Alambagh - Primary School Room No. 1", "voters": 578, "lat": 26.8124, "lon": 80.9105, "hv": 0.0734, "hm": 0.1692},
        {"id": 2, "name": "Alambagh - Primary School Room No. 2", "voters": 577, "lat": 26.8128, "lon": 80.9109, "hv": 0.0806, "hm": 0.2291},
        {"id": 3, "name": "Singar Nagar - Junior High School East Wing", "voters": 657, "lat": 26.8045, "lon": 80.9012, "hv": 0.0783, "hm": 0.1604},
        {"id": 4, "name": "Singar Nagar - Junior High School West Wing", "voters": 641, "lat": 26.8049, "lon": 80.9016, "hv": 0.0796, "hm": 0.1638},
        {"id": 5, "name": "Krishna Nagar - Inter College Central Room", "voters": 511, "lat": 26.7925, "lon": 80.8878, "hv": 0.0789, "hm": 0.2115},
        {"id": 6, "name": "Krishna Nagar - Government School North Hall", "voters": 543, "lat": 26.7929, "lon": 80.8882, "hv": 0.0723, "hm": 0.2085},
        {"id": 7, "name": "Cantt Area - Community Hall Room No. 1", "voters": 535, "lat": 26.8185, "lon": 80.9525, "hv": 0.1003, "hm": 0.4065},
        {"id": 8, "name": "Cantt Area - Primary School Room No. 1", "voters": 523, "lat": 26.8189, "lon": 80.9529, "hv": 0.1031, "hm": 0.4152},
        {"id": 9, "name": "Sadar Bazar - Primary School Room No. 2", "voters": 587, "lat": 26.8295, "lon": 80.9602, "hv": 0.0724, "hm": 0.0424},
        {"id": 10, "name": "Sadar Bazar - Junior High School East Wing", "voters": 616, "lat": 26.8299, "lon": 80.9606, "hv": 0.0713, "hm": 0.0403},
        {"id": 11, "name": "Charbagh - Junior High School West Wing", "voters": 616, "lat": 26.8221, "lon": 80.9325, "hv": 0.0653, "hm": 0.0434},
        {"id": 12, "name": "Charbagh - Inter College Central Room", "voters": 610, "lat": 26.8225, "lon": 80.9329, "hv": 0.0664, "hm": 0.0278},
        {"id": 13, "name": "Nilmatha - Government School North Hall", "voters": 554, "lat": 26.7845, "lon": 80.9852, "hv": 0.1012, "hm": 0.4107},
        {"id": 14, "name": "Nilmatha - Community Hall Room No. 1", "voters": 549, "lat": 26.7849, "lon": 80.9856, "hv": 0.1023, "hm": 0.4144},
        {"id": 15, "name": "Amausi - Primary School Room No. 1", "voters": 582, "lat": 26.7625, "lon": 80.8805, "hv": 0.0772, "hm": 0.1375}
    ]
    
    # 96 strata definitions: Gender (2) * Age (4) * Social Category (3) * Occupation (4)
    genders = ["Male", "Female"]
    age_groups = ["18-25", "26-35", "36-50", "51+"]
    social_groups = ["General/OBC", "SC", "ST"]
    occupations = ["Cultivator", "Ag-Laborer", "Other-Worker", "Non-Worker"]
    
    # Make sure target directories exist
    os.makedirs("/Users/vinodh/debaz/nethra/data", exist_ok=True)
    
    # 1. Generate poststratification_frame.csv
    frame_path = "/Users/vinodh/debaz/nethra/data/poststratification_frame.csv"
    with open(frame_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["booth_id", "gender", "age_group", "social_group", "occupation", "n_voters"])
        
        for b in booths:
            b_id = b["id"]
            total_v = b["voters"]
            
            # Generate 96 cells of mock demographics with random distribution summing to total_v
            # Make sure some cells are very sparse to test the k-anonymity merging engine!
            raw_weights = [random.expovariate(1.0) for _ in range(96)]
            sum_weights = sum(raw_weights)
            normalized_counts = [max(1, int((w / sum_weights) * total_v)) for w in raw_weights]
            
            # Adjust difference due to rounding
            diff = total_v - sum(normalized_counts)
            for i in range(abs(diff)):
                idx = random.randint(0, 95)
                if diff > 0:
                    normalized_counts[idx] += 1
                elif diff < 0 and normalized_counts[idx] > 1:
                    normalized_counts[idx] -= 1
                    
            cell_idx = 0
            for g in genders:
                for a in age_groups:
                    for s in social_groups:
                        for o in occupations:
                            writer.writerow([b_id, g, a, s, o, normalized_counts[cell_idx]])
                            cell_idx += 1
                            
    print(f"Generated poststratification frame at: {frame_path}")
    
    # 2. Generate booth_covariates.csv
    cov_path = "/Users/vinodh/debaz/nethra/data/booth_covariates.csv"
    with open(cov_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "booth_id", "lat", "lon", "wealth_index", 
            "dilapidated_house_ratio", "electricity_access_ratio", 
            "sanitation_deprivation_ratio", "bank_distance_km", 
            "mobile_coverage_status", "power_hours_domestic",
            "historical_volatility_index", "historical_margin_of_victory"
        ])
        
        for b in booths:
            b_id = b["id"]
            # Generate realistic deprivation indices based on booth locations
            # Strongholds (Cantt/Nilmatha - Booths 7, 8, 13, 14) are modeled as wealthier urban zones
            # Swing booths (Sadar Bazar - Booths 9, 10, 11, 12) are modeled as highly volatile density zones
            if b_id in [7, 8, 13, 14]:
                wealth = round(random.uniform(0.65, 0.90), 2)
                dilapidated = round(random.uniform(0.02, 0.08), 2)
                electricity = round(random.uniform(0.95, 0.99), 2)
                sanitation = round(random.uniform(0.01, 0.05), 2)
                bank_dist = round(random.uniform(0.2, 1.2), 2)
                mobile = 1
                power_hours = random.randint(20, 24)
            else:
                wealth = round(random.uniform(0.30, 0.58), 2)
                dilapidated = round(random.uniform(0.12, 0.28), 2)
                electricity = round(random.uniform(0.78, 0.92), 2)
                sanitation = round(random.uniform(0.15, 0.35), 2)
                bank_dist = round(random.uniform(1.5, 4.8), 2)
                mobile = 1 if random.random() > 0.1 else 0
                power_hours = random.randint(14, 18)
                
            writer.writerow([
                b_id, b["lat"], b["lon"], wealth,
                dilapidated, electricity, sanitation, bank_dist,
                mobile, power_hours, b["hv"], b["hm"]
            ])
            
    print(f"Generated booth covariates at: {cov_path}")

if __name__ == "__main__":
    generate_data()
