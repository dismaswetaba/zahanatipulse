
-- =========================================
-- 1. FACILITIES
-- =========================================

CREATE TABLE facilities (
    facility_id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    location VARCHAR(150),
    phone VARCHAR(30),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- =========================================
-- 2. USERS
-- =========================================

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    facility_id INTEGER NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,

    role VARCHAR(20) NOT NULL
        CHECK (role IN (
            'admin',
            'receptionist',
            'clinician',
            'pharmacist'
        )),

    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_users_facility
        FOREIGN KEY (facility_id)
        REFERENCES facilities(facility_id),

    CONSTRAINT uq_users_facility_user
        UNIQUE (facility_id, user_id)
);


-- =========================================
-- 3. PATIENTS
-- =========================================

CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,
    facility_id INTEGER NOT NULL,
    patient_number VARCHAR(30) NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    date_of_birth DATE,
    phone VARCHAR(30),
    created_by INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_patients_facility
        FOREIGN KEY (facility_id)
        REFERENCES facilities(facility_id),

    CONSTRAINT fk_patients_creator
        FOREIGN KEY (facility_id, created_by)
        REFERENCES users(facility_id, user_id),

    CONSTRAINT uq_patient_number_per_facility
        UNIQUE (facility_id, patient_number),

    CONSTRAINT uq_patient_facility_id
        UNIQUE (facility_id, patient_id)
);


-- =========================================
-- 4. APPOINTMENTS
-- =========================================

CREATE TABLE appointments (
    appointment_id SERIAL PRIMARY KEY,
    facility_id INTEGER NOT NULL,
    patient_id INTEGER NOT NULL,
    appointment_datetime TIMESTAMPTZ NOT NULL,
    service VARCHAR(100) NOT NULL,

    status VARCHAR(20) NOT NULL DEFAULT 'Scheduled'
        CHECK (status IN (
            'Scheduled',
            'Completed',
            'Cancelled'
        )),

    created_by INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_appointments_patient
        FOREIGN KEY (facility_id, patient_id)
        REFERENCES patients(facility_id, patient_id),

    CONSTRAINT fk_appointments_creator
        FOREIGN KEY (facility_id, created_by)
        REFERENCES users(facility_id, user_id),

    CONSTRAINT uq_appointment_facility_patient_id
        UNIQUE (facility_id, patient_id, appointment_id)
);


-- =========================================
-- 5. QUEUE ENTRIES
-- =========================================

CREATE TABLE queue_entries (
    queue_entry_id SERIAL PRIMARY KEY,
    facility_id INTEGER NOT NULL,
    patient_id INTEGER NOT NULL,
    appointment_id INTEGER,
    queue_number INTEGER NOT NULL,
    queue_date DATE NOT NULL DEFAULT CURRENT_DATE,
    department VARCHAR(50) NOT NULL,

    status VARCHAR(20) NOT NULL DEFAULT 'Waiting'
        CHECK (status IN (
            'Waiting',
            'Called',
            'In Service',
            'Completed',
            'Cancelled'
        )),

    issued_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    called_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,

    CONSTRAINT fk_queue_patient
        FOREIGN KEY (facility_id, patient_id)
        REFERENCES patients(facility_id, patient_id),

    CONSTRAINT fk_queue_appointment
        FOREIGN KEY (facility_id, patient_id, appointment_id)
        REFERENCES appointments(
            facility_id,
            patient_id,
            appointment_id
        ),

    CONSTRAINT uq_queue_number
        UNIQUE (
            facility_id,
            queue_date,
            department,
            queue_number
        )
);


-- =========================================
-- 6. MEDICINES
-- =========================================

CREATE TABLE medicines (
    medicine_id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    strength VARCHAR(50),
    form VARCHAR(50)
);


-- =========================================
-- 7. INVENTORY
-- =========================================

CREATE TABLE inventory (
    inventory_id SERIAL PRIMARY KEY,
    facility_id INTEGER NOT NULL,
    medicine_id INTEGER NOT NULL,

    quantity INTEGER NOT NULL DEFAULT 0
        CHECK (quantity >= 0),

    reorder_level INTEGER NOT NULL DEFAULT 10
        CHECK (reorder_level >= 0),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_inventory_facility
        FOREIGN KEY (facility_id)
        REFERENCES facilities(facility_id),

    CONSTRAINT fk_inventory_medicine
        FOREIGN KEY (medicine_id)
        REFERENCES medicines(medicine_id),

    CONSTRAINT uq_facility_medicine
        UNIQUE (facility_id, medicine_id),

    CONSTRAINT uq_inventory_facility_id
        UNIQUE (facility_id, inventory_id)
);


-- =========================================
-- 8. STOCK MOVEMENTS
-- =========================================

CREATE TABLE stock_movements (
    movement_id SERIAL PRIMARY KEY,
    facility_id INTEGER NOT NULL,
    inventory_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,

    movement_type VARCHAR(20) NOT NULL
        CHECK (movement_type IN ('received', 'issued')),

    quantity_changed INTEGER NOT NULL
        CHECK (quantity_changed > 0),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_movement_inventory
        FOREIGN KEY (facility_id, inventory_id)
        REFERENCES inventory(facility_id, inventory_id),

    CONSTRAINT fk_movement_user
        FOREIGN KEY (facility_id, user_id)
        REFERENCES users(facility_id, user_id)
);


-- =========================================
-- 9. INDEXES
-- =========================================

CREATE INDEX idx_patients_name
    ON patients (facility_id, full_name);

CREATE INDEX idx_appointments_date
    ON appointments (facility_id, appointment_datetime);

CREATE INDEX idx_queue_today
    ON queue_entries (facility_id, queue_date, status);

CREATE INDEX idx_appointments_patient
    ON appointments (patient_id);

CREATE INDEX idx_queue_patient
    ON queue_entries (patient_id);

CREATE INDEX idx_stock_movements_inventory
    ON stock_movements (inventory_id);

CREATE INDEX idx_stock_movements_user
    ON stock_movements (user_id);