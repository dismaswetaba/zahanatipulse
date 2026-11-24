DROP TABLE IF EXISTS stock_movements, inventory, medicines, queue_entries,
    appointments, patients, users, facilities CASCADE;

CREATE TABLE facilities (
    facility_id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    location VARCHAR(150),
    phone VARCHAR(30),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    facility_id INTEGER NOT NULL REFERENCES facilities(facility_id),
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) NOT NULL
        CHECK (role IN ('admin','receptionist','clinician','pharmacist')),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,
    facility_id INTEGER NOT NULL REFERENCES facilities(facility_id),
    patient_number VARCHAR(30) NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    date_of_birth DATE,
    phone VARCHAR(30),
    created_by INTEGER REFERENCES users(user_id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (facility_id, patient_number)
);

CREATE TABLE appointments (
    appointment_id SERIAL PRIMARY KEY,
    facility_id INTEGER NOT NULL REFERENCES facilities(facility_id),
    patient_id INTEGER NOT NULL REFERENCES patients(patient_id),
    appointment_datetime TIMESTAMP NOT NULL,
    service VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Scheduled'
        CHECK (status IN ('Scheduled','Completed','Cancelled')),
    created_by INTEGER REFERENCES users(user_id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE queue_entries (
    queue_entry_id SERIAL PRIMARY KEY,
    facility_id INTEGER NOT NULL REFERENCES facilities(facility_id),
    patient_id INTEGER NOT NULL REFERENCES patients(patient_id),
    appointment_id INTEGER REFERENCES appointments(appointment_id),
    queue_number INTEGER NOT NULL,
    queue_date DATE NOT NULL DEFAULT CURRENT_DATE,
    department VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Waiting'
        CHECK (status IN ('Waiting','Called','In Service','Completed','Cancelled')),
    issued_at TIMESTAMP NOT NULL DEFAULT NOW(),
    called_at TIMESTAMP,
    completed_at TIMESTAMP,
    UNIQUE (facility_id, queue_date, department, queue_number)
);

CREATE TABLE medicines (
    medicine_id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    strength VARCHAR(50),
    form VARCHAR(50)
);

CREATE TABLE inventory (
    inventory_id SERIAL PRIMARY KEY,
    facility_id INTEGER NOT NULL REFERENCES facilities(facility_id),
    medicine_id INTEGER NOT NULL REFERENCES medicines(medicine_id),
    quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    reorder_level INTEGER NOT NULL DEFAULT 10 CHECK (reorder_level >= 0),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (facility_id, medicine_id)
);

CREATE TABLE stock_movements (
    movement_id SERIAL PRIMARY KEY,
    inventory_id INTEGER NOT NULL REFERENCES inventory(inventory_id),
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    movement_type VARCHAR(20) NOT NULL
        CHECK (movement_type IN ('received','issued')),
    quantity_changed INTEGER NOT NULL CHECK (quantity_changed > 0),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_patients_name ON patients (facility_id, full_name);
CREATE INDEX idx_appointments_date ON appointments (facility_id, appointment_datetime);
CREATE INDEX idx_queue_today ON queue_entries (facility_id, queue_date, status);
