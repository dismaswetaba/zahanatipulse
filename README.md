# MENTAL HEALTH DETECTOR
ZahanatiPulse
System Architecture Document | Version 1.0 | Hackathon MVP
1. Project Overview
ZahanatiPulse is a web-based healthcare facility management and patient-flow platform. It aims to digitize and streamline patient registration, appointments, queues, medicine inventory, and operational monitoring. The system supports multiple healthcare facilities through one centralized application while keeping each facility’s patient records and operational data separate.
Problem Statement
Healthcare facilities may experience slow registration and record retrieval, poorly organized queues, appointment-management challenges, limited medicine-stock visibility, and difficulty monitoring facility operations. ZahanatiPulse proposes a unified digital system for these administrative workflows.
Objectives
Digitize patient registration and record retrieval.
Manage appointments and patient attendance.
Organize queues and patient service flow.
Track facility medicine stock and stock movements.
Provide facility-level dashboards and operational reports.
Support multiple facilities while enforcing data isolation.
Provide a foundation for future operational AI-assisted insights.
2. Users and Roles
Role	Responsibilities
Administrator	Manage facility users, settings, dashboards and operational reports.
Receptionist	Register patients, search records, create and manage appointments, and manage patient queue entry.
Clinician	View authorised patient information and update relevant patient service workflow.
Pharmacist	Manage medicine stock, inventory records, and stock movements.
3. Architecture
ZahanatiPulse uses a three-tier architecture:
Presentation Layer (Frontend): HTML5, CSS3 and JavaScript. Displays forms, dashboards, tables, navigation and responsive user interfaces. Sends requests to the backend.
Application Layer (Backend): Python and Flask. Handles authentication, permissions, facility isolation, validation, business rules, API endpoints and workflows.
Data Layer: SQLite for the MVP. Stores facilities, staff accounts, patients, appointments, queue entries, medicine catalogue, inventory and stock movements.
Optional AI integration: an external AI service may be called by the Flask backend for non-clinical operational summaries. The core system must continue functioning if AI is unavailable.
4. Technology Stack
Technology	Purpose
HTML5	Web page structure
CSS3	Layout, styling and responsive design
JavaScript	Frontend interactions and backend API communication
Python	Backend logic
Flask	Web framework and REST API
SQLite	Relational database for the MVP
Chart.js	Optional dashboard data visualizations
Git and GitHub	Version control and team collaboration
5. Multi-Facility Design
The platform serves multiple facilities using one application and database. Every facility-related record is associated with a facility_id. Staff access is restricted to their authorised facility or facilities. Patient records are facility-specific: if the same person visits another facility, that facility registers a separate patient record in the MVP. Patient numbers are unique within a facility, not necessarily across the entire platform.
Facility-owned data includes staff accounts, patients, appointments, queue entries, inventory and reports. Cross-facility medicine availability may be exposed to authorised users without sharing patient records.
6. Database Design (Initial Tables)
Table	Initial fields
facilities	id, name, location, phone, created_at
users	id, facility_id, full_name, email, password_hash, role, is_active, created_at
patients	id, facility_id, patient_number, full_name, date_of_birth, phone, created_by, created_at
appointments	id, facility_id, patient_id, appointment_datetime, service, status, created_by, created_at
queue_entries	id, facility_id, patient_id, appointment_id (nullable), queue_number, queue_date, department, status, issued_at, called_at, completed_at
medicines	id, name, strength, form
inventory	id, facility_id, medicine_id, quantity, reorder_level, updated_at
stock_movements	id, inventory_id, user_id, movement_type, quantity_changed, created_at
Design constraints to confirm: patient_number unique per facility; inventory unique per facility and medicine; queue numbers unique per facility and queue date; foreign keys enforced. The final schema and cardinalities will be reviewed before implementation.
7. Core Modules
Dashboard: Facility operational metrics: visits, appointments, queue size, stock alerts and summary charts.
Patient Management: Register patients, generate facility patient numbers, search, view and update records.
Appointments: Create, list, reschedule, cancel and track appointments.
Queue Management: Issue queue numbers, view waiting patients, call next, and update service statuses.
Medicine Inventory: Maintain stock, record receipts/issues/adjustments, show stock history and low-stock alerts.
Reports and Analytics: Facility-specific attendance, appointment, queue and inventory reports.
8. Workflow Summaries
Patient Registration
Receptionist logs in → enters patient details → frontend submits to Flask → backend authenticates, checks facility, validates details and generates a patient number → record is stored in SQLite → confirmation is returned.
Appointment
Receptionist searches for the facility patient → selects the patient → enters service and date/time → backend validates and stores appointment → appointment appears in the facility schedule.
Queue
Patient arrives → reception confirms registration and service → queue number is generated → staff calls the patient → status is updated as service proceeds and completes.
Inventory
Pharmacist records stock receipt, issue or adjustment → backend validates movement → inventory balance and movement history update → low-stock alert is generated if quantity is at or below reorder level.
9. Backend Structure (Proposed)
ZahanatiPulse/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── patients.py
│   │   ├── appointments.py
│   │   ├── queue.py
│   │   ├── inventory.py
│   │   ├── reports.py
│   │   └── ai.py
│   ├── services/
│   │   ├── patient_service.py
│   │   ├── appointment_service.py
│   │   ├── queue_service.py
│   │   ├── inventory_service.py
│   │   └── analytics_service.py
│   ├── database/
│   │   ├── connection.py
│   │   ├── schema.sql
│   │   └── seed.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── patients/
│   │   ├── appointments/
│   │   ├── queue/
│   │   └── inventory/
│   └── static/
│       ├── css/
│       ├── js/
│       ├── images/
│       └── icons/
├── instance/
│   └── zahanatipulse.db
├── tests/
├── requirements.txt
├── run.py
├── .env
├── .gitignore
└── README.md
10. Frontend Navigation
Proposed navigation: Dashboard; Patients; Appointments; Queue Management; Medicine Inventory; Reports; User Management (Administrator); Settings; Logout.
Frontend responsibilities: render forms and tables, perform basic client-side validation, submit API requests, display results and errors, and support responsive layouts. Backend validation and permission checks remain authoritative.
11. Proposed API Endpoints
Method	Endpoint	Purpose
POST	/api/auth/login	Authenticate user
POST	/api/auth/logout	Logout
GET	/api/dashboard	Retrieve facility dashboard
GET	/api/patients	Search/list facility patients
POST	/api/patients	Register patient
GET	/api/patients/<id>	Retrieve patient record
PUT	/api/patients/<id>	Update patient
GET	/api/appointments	List appointments
POST	/api/appointments	Create appointment
PUT	/api/appointments/<id>	Update appointment
GET	/api/queue	View queue
POST	/api/queue	Add queue entry
PUT	/api/queue/<id>	Update queue entry
GET	/api/inventory	View inventory
POST	/api/inventory/movements	Record stock movement
GET	/api/reports	Retrieve facility reports
These are proposed contracts; exact request/response formats, validation rules and endpoint details will be finalised during implementation.
12. Security and Privacy
Password hashes, never plain-text passwords.
Authenticated sessions and protected endpoints.
Role-based authorization enforced in Flask.
Facility-level data isolation enforced by backend queries and access checks.
Input validation and parameterized database queries.
Secrets and API keys kept out of source control.
Use fictional patient data for development and demonstrations.
Avoid unnecessary patient details in logs, URLs and AI requests.
Foreign keys, uniqueness constraints and appropriate transactions to protect data integrity.
13. Optional AI Integration
AI is an optional supporting capability, not a core dependency. Possible MVP-safe use cases include summarising facility-level operational metrics, describing queue patterns and generating non-clinical report summaries from anonymised or aggregated data. AI must not diagnose, prescribe, make treatment decisions or replace clinicians. Requests to an external AI provider go through Flask; credentials are never exposed in the browser. If AI is unavailable, core modules continue to work.
14. Cross-Facility Medicine Availability (Potential Feature)
Authorised users may be able to view medicine availability across participating facilities. This feature shows stock availability only; it does not automatically reserve, transfer or dispense medicine. It is a potential differentiator, but should not delay the core inventory module.
15. Development and Deployment
Hackathon development and demonstration can run locally on a laptop using Flask and SQLite. Internet hosting is not required for a local demonstration. For future production deployment, the system would require HTTPS, production hosting, stronger operational monitoring, backups and recovery, security testing, compliance review, and likely migration to a database such as PostgreSQL.
16. MVP Scope
Must-have
Login and role-based access
Multi-facility support and facility data isolation
Patient registration and search
Appointment management
Queue management
Medicine inventory and low-stock alerts
Facility dashboard and basic operational statistics
If time permits
Cross-facility medicine availability
Advanced reports
AI-generated operational summaries or queue insights
SMS notifications
Digital referrals
17. Team Collaboration
Suggested areas: project coordination and integration; frontend; backend; database. Team members may take more than one area. Shared responsibilities include testing, review, documentation and demo preparation.
Develop features on branches, not directly on main.
Agree on database schema and API contracts before parallel development.
Commit and push regularly.
Review and test changes before merging.
Do not commit secrets, credentials, or real patient data.
Communicate before changing shared interfaces or schema.
18. Development Roadmap
1.Requirements and system design: finalise scope, roles, schema, constraints, API contracts and workflows.
2.Database implementation: create schema, constraints and fictional seed data.
3.Backend foundation: Flask setup, authentication, role permissions and facility isolation.
4.Patient and appointment modules.
5.Queue management module.
6.Inventory module.
7.Frontend integration and dashboard.
8.Testing, debugging, access-control checks and demo preparation.
9.Optional enhancements only after the core MVP is stable.
19. Design Principles
Clarity before coding: confirm requirements and interfaces first.
Build a working MVP instead of many incomplete features.
Keep modules understandable and reasonably separated.
Backend enforces validation, authorization and facility isolation.
Use fictional data for demonstrations.
AI is optional; core functionality must not depend on it.
Team members should understand and be able to explain the code they contribute.
20. Architecture Summary
ZahanatiPulse is a centralized, multi-facility web application using HTML, CSS and JavaScript on the frontend; Python Flask for backend services and REST endpoints; and SQLite for the hackathon database. Facility-specific users, patients, appointments, queues and inventory are isolated through facility-aware authorization and database relationships. Core modules include patient management, appointments, queues, inventory, dashboards and reports. AI and cross-facility medicine visibility are optional enhancements.
This document describes the proposed architecture, not a completed or production-ready healthcare system. The schema, access rules, endpoint contracts and workflow details must be reviewed and agreed before implementation.