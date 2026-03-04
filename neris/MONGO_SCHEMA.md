# NERIS MongoDB Document Schema

## Collection: `incidents`
This is the primary collection for all fire department incident reports.

### Document Structure
```json
{
  "_id": "ObjectId",
  "neris_id": "string",       // Unique: EntityID:Epoch
  "internal_id": "string",    // Department's local ID
  "status": "string",        // draft, validated, submitted, error
  "last_synced": "date",
  
  "core": {
    "type_identifiers": {
      "final_types": "Array[Array[Text]]", // Multi-level types
      "primary_index": "int"
    },
    "location": {
      "point": { "type": "Point", "coordinates": [lng, lat] },
      "address": "Object (mod_civic_location)",
      "location_use": "string",
      "people_present": "boolean"
    }
  },

  "modules": {
    "fire": "Object (mod_fire) | null",
    "medical": "Array[mod_medical]",
    "hazsit": "Object (mod_hazard) | null",
    "rescues": {
      "firefighter": "Array[mod_rescue_ff]",
      "civilian": "Array[mod_rescue_nonff]"
    }
  },

  "unit_responses": "Array[mod_unit_response]",
  "narrative": {
    "impediments": "string",
    "outcome": "string"
  }
}
```

## Collection: `lookups`
Caches NERIS "Value Sets" for frontend dropdowns.
```json
{
  "key": "type_incident",
  "values": [
    { "code": "100", "description": "Fire", "level": 1 }
  ],
  "last_updated": "date"
}
```
