# NERIS Schema Research & Mapping

## 1. Module Deep Dive: `core_mod_incident`
The root document for every incident. 
*   **Key IDs:** `neris_id` (EntityID:Epoch) and `internal_id`.
*   **Logical Forks:** The incident type determines which sub-modules are required.
*   **GeoJSON:** `incident_point` maps to standard coordinates.

## 2. Module Deep Dive: `mod_fire`
Injected when the incident type includes "Fire".
*   **Hard Conditional Fork:** 
    *   `structure_fire`: Requires Building Origin, Floor, Room, and Damage level.
    *   `outside_fire`: Requires Acres Burned and Outside Cause.
*   **Mandatory Field:** `fire_investigation_need` (Must be TRUE/FALSE).

## 3. Module Deep Dive: `mod_civic_location`
Uses CLDXF (Community Location Data Exchange Format).
*   **Granularity:** Addresses are split into Number, Pre-Dir, Street Name, Post-Type, etc.
*   **Precision:** Supports `nl_floor`, `nl_room`, and `nl_seat`.
*   **Geocoding:** Points are prioritized over address strings.

## 4. Proposed MongoDB Document Mapping
```json
{
  "neris_id": "string",
  "internal_id": "string",
  "core": {
    "location": { "point": "GeoJSON", "address": "CLDXF Module" },
    "types": "Array[Array[Text]]"
  },
  "modules": {
    "fire": "Embedded mod_fire object",
    "medical": "Array of mod_medical objects"
  }
}
```
