# NERIS Implementation Plan

## Overview
A Django 6 / Vue 3 / MongoDB system for fire departments to collect and submit data to the National Emergency Response Information System (NERIS). This system handles the modular, hierarchical nature of fire reporting while providing a user-friendly, non-technical interface for department personnel.

## Technical Stack
*   **Backend:** Django 6 (Python) using `pymongo` for incident data and SQLite for auth.
*   **Frontend:** Vue 3 (Composition API) with a JSON-driven dynamic form engine.
*   **Database:** MongoDB 7 (Flexible schema for modular NERIS data).
*   **Authentication:** JWT (SimpleJWT) for stateless session management.
*   **Integration:** NERIS REST API (FastAPI).

## Phase 1: Research & Schema Mapping (COMPLETED)
*   [x] Initial scan of NERIS Technical Reference.
*   [x] Identification of Core vs. Secondary schemas.
*   [x] Extract field-level requirements for `core_mod_incident`.
*   [x] Define MongoDB document structure for standard incidents.

## Phase 2: Core System Architecture (COMPLETED)
*   [x] **Dynamic Forms:** Build a recursive Vue engine to render nested NERIS modules (Fire, Medical, etc.).
*   [x] **Validation Engine:** Server-side recursive check for `db_required` and `neris_core` constraints.
*   [x] **Lookup Service:** Automated synchronization of NERIS "Value Sets" (Enumerations).
*   [x] **Authentication:** JWT-based login for department personnel (McCool, Shell, Mud).

## Phase 3: Development Modules (IN PROGRESS)
*   [x] **Seeded Demo Environment:** Fictional "Lobster Cove Fire & Rescue" station, fleet, and personnel.
*   [x] **Incident Dashboard:** Centralized view for CAD feeds, drafts, and resource status.
*   [ ] **CAD Integration:** One-click pre-filling of reports from dispatch data.
*   [ ] **Submission Pipeline:** Final handshake with the NERIS FastAPI using OAuth2.

## Next Steps
1.  **Map CAD to Incident:** Write the mapping logic to turn raw dispatch events into pre-filled incident documents.
2.  **API Submission:** Implement the `submit_to_neris` method in the viewset using the `neris-api-client`.
3.  **UI Polish:** Add the "Validation Sidebar" jump-to links and field highlighting.
