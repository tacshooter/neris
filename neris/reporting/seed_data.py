from reporting.db import MongoDB
from datetime import datetime, timedelta
import os
import django

# Setup Django environment for standalone run
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neris_backend.settings')
django.setup()

def seed_lobster_cove():
    db = MongoDB.get_db()
    
    # 1. Department Info
    db.departments.update_one(
        {"neris_id": "FD_LOBSTER_001"},
        {"$set": {
            "name": "Lobster Cove Fire & Rescue",
            "state": "ME",
            "hq_address": "100 Pier Rd, Lobster Cove, ME",
            "stations": [
                {"id": "STN10", "name": "Station 10 - Main", "location": {"type": "Point", "coordinates": [-69.8, 43.8]}},
                {"id": "STN20", "name": "Station 20 - North", "location": {"type": "Point", "coordinates": [-69.75, 43.85]}}
            ]
        }}, upsert=True
    )

    # 2. Units (Trucks)
    units = [
        {"unit_id": "E10", "type": "Engine", "station": "STN10", "staffing": 4},
        {"unit_id": "T10", "type": "Truck/Aerial", "station": "STN10", "staffing": 3},
        {"unit_id": "R10", "type": "Rescue/EMS", "station": "STN10", "staffing": 2},
        {"unit_id": "E20", "type": "Engine", "station": "STN20", "staffing": 3}
    ]
    db.units.delete_many({}) 
    db.units.insert_many(units)

    # 3. Personnel & Users
    from django.contrib.auth.models import User
    
    personnel_data = [
        {"name": "Capt. Finn McCool", "username": "mccool", "rank": "Captain", "id": "P101"},
        {"name": "FF Sarah Shell", "username": "shell", "rank": "Firefighter", "id": "P102"},
        {"name": "Para Mike Mud", "username": "mud", "rank": "Paramedic", "id": "P103"},
    ]
    
    db.personnel.delete_many({})
    for p in personnel_data:
        # Create Django user for Auth
        user, created = User.objects.get_or_create(username=p['username'])
        if created:
            user.set_password('lobster123') # Default demo password
            user.save()
        
        # Create Personnel record for app data
        db.personnel.insert_one({
            "name": p['name'],
            "rank": p['rank'],
            "id": p['id'],
            "username": p['username']
        })

    # 4. Mock CAD Feed (Incoming Incidents)
    # We use string datetimes for ease of JSON serialization in this mock
    now = datetime.now()
    cad_events = [
        {
            "cad_id": "CAD-2026-0001",
            "type_hierarchy": ["FIRE", "STRUCTURE_FIRE", "RESIDENTIAL"],
            "address": "45 Oyster Ln",
            "dispatched_at": (now - timedelta(hours=2)).isoformat(),
            "units": ["E10", "T10", "R10"],
            "narrative_initial": "Structure fire, heavy smoke from Alpha side."
        },
        {
            "cad_id": "CAD-2026-0002",
            "type_hierarchy": ["MEDICAL", "ILLNESS", "CARDIAC_ARREST"],
            "address": "Lobster Cove Pier",
            "dispatched_at": (now - timedelta(minutes=45)).isoformat(),
            "units": ["R10"],
            "narrative_initial": "65M unconscious on pier."
        },
        {
            "cad_id": "CAD-2026-0003",
            "type_hierarchy": ["HAZSIT", "HAZMAT", "FUEL_SPILL"],
            "address": "Gas n Go Station #4",
            "dispatched_at": (now - timedelta(days=1)).isoformat(),
            "units": ["E20"],
            "narrative_initial": "Gasoline spill near pump 3."
        }
    ]
    db.cad_feed.delete_many({})
    db.cad_feed.insert_many(cad_events)
    
    # 5. Existing Drafts (to show on dashboard)
    drafts = [
        {
            "neris_id": "FD_LOBSTER_001:1741000000",
            "internal_id": "LCFR-26-010",
            "status": "draft",
            "data": {
                "incident_final_type": [["FIRE", "STRUCTURE_FIRE", "RESIDENTIAL"]],
                "location": {"an_number": 45, "sn_street_name": "Oyster", "sn_post_type": "Ln"}
            },
            "created_at": (now - timedelta(hours=1)).isoformat()
        }
    ]
    db.incidents.delete_many({"neris_id": "FD_LOBSTER_001:1741000000"})
    db.incidents.insert_many(drafts)

    print("Successfully seeded Lobster Cove Fire & Rescue data.")

if __name__ == "__main__":
    seed_lobster_cove()
