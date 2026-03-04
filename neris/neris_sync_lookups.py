import yaml
import json
import requests
import sys

BASE_URL = "https://raw.githubusercontent.com/ulfsri/neris-framework/main/core_schemas/value_sets/yml/"

# List of common value sets to sync
VALUE_SETS = [
    "type_incident",
    "type_special_modifier",
    "type_suppress_appliance",
    "type_water_supply",
    "type_fire_invest_need",
    "type_fire_bldg_damage",
    "type_room",
    "type_fire_cause_in"
]

def fetch_value_set(name):
    url = f"{BASE_URL}{name}.yml"
    print(f"Fetching {url}...")
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return yaml.safe_load(response.text)

def process_value_set(name, data):
    processed = {
        "key": name,
        "options": []
    }
    
    for key, attrs in data.items():
        if attrs.get('active', 'TRUE').upper() != 'TRUE':
            continue
            
        entry = {
            "code": key,
            "levels": []
        }
        
        # Capture up to 3 levels of hierarchy
        for i in range(1, 4):
            val = attrs.get(f'value_{i}')
            desc = attrs.get(f'description_{i}')
            if val:
                entry["levels"].append({"value": val, "description": desc})
        
        # Add NFIRS crosswalk if present
        if 'NFIRS Crosswalk' in attrs:
            entry["nfirs_codes"] = [c.strip() for c in str(attrs['NFIRS Crosswalk']).split(',')]
            
        processed["options"].append(entry)
        
    return processed

if __name__ == "__main__":
    all_lookups = []
    for vs in VALUE_SETS:
        raw_data = fetch_value_set(vs)
        if raw_data:
            all_lookups.append(process_value_set(vs, raw_data))
            
    with open("neris_lookups.json", "w") as f:
        json.dump(all_lookups, f, indent=2)
    print(f"Sync complete. Output saved to neris_lookups.json")
