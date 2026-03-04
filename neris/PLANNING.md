# NERIS Implementation Plan

## Overview
A Django/Vue.js system for fire departments to collect and submit data to the National Emergency Response Information System (NERIS), utilizing MongoDB for flexible schema management. This system aims to provide a user-friendly interface for manual data entry while ensuring compatibility with the NERIS V1 Data Exchange standards.

## Technical Stack
*   **Backend:** Django (Python) with MongoDB integration (likely using `djongo` or `pymongo` directly).
*   **Frontend:** Vue 3 (Composition API) with a dynamic form engine.
*   **Database:** MongoDB (to handle the evolving and modular NERIS schema).
*   **Integration:** NERIS REST API (FastAPI) for data submission and value set synchronization.

## Phase 1: Research & Schema Mapping
*   [x] Initial scan of NERIS Technical Reference.
*   [x] Identification of Core vs. Secondary schemas.
*   [ ] Extract field-level requirements for `core_mod_incident`.
*   [ ] Define MongoDB document structure for standard incidents.
*   [ ] Map NERIS `possible_if` logic to frontend form state.

## Phase 2: Core System Architecture
*   **Dynamic Forms:** Build a Vue component that renders forms based on NERIS module definitions.
*   **Validation Engine:** Implement server-side validation to match `db_required` and `neris_core` constraints.
*   **Lookup Service:** Automated caching of NERIS "Value Sets" (enumerations) from GitHub/API to populate dropdowns.
*   **API Client:** Integration with the `neris-api-client` for secure data transfer.

## Phase 3: Development Modules
1.  **Authentication & Profile:** Fire department entity setup and user management.
2.  **Incident Reporting:** Step-by-step wizard for incident data entry.
3.  **CAD Integration (Optional):** Future expansion for dispatch data import.
4.  **Submission Dashboard:** Track status of submitted records and compatibility badges.

## Next Steps
*   Deep dive into `core_mod_incident.yml` to extract a concrete example of data requirements.
*   Propose a MongoDB schema for an incident document.
*   Review NERIS API authentication requirements (OAuth2).
