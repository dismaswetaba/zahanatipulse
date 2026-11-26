-- Fictional demo data only. Demo password for every user is set in seed.py.

INSERT INTO facilities (name, location, phone) VALUES
('Meru Health Centre',   'Meru',   '0700 000 001'),
('Kisumu Health Centre', 'Kisumu', '0700 000 002');

INSERT INTO users (facility_id, full_name, email, password_hash, role) VALUES
(1, 'Grace Kinyua',       'admin.meru@zahanatipulse.test',        '__PASSWORD_HASH__', 'admin'),
(1, 'Peter Mwiti',        'reception.meru@zahanatipulse.test',    '__PASSWORD_HASH__', 'receptionist'),
(1, 'Dr. Faith Kaimenyi', 'clinician.meru@zahanatipulse.test',    '__PASSWORD_HASH__', 'clinician'),
(1, 'Joseph Mutua',       'pharmacy.meru@zahanatipulse.test',     '__PASSWORD_HASH__', 'pharmacist'),
(2, 'Achieng Odhiambo',   'admin.kisumu@zahanatipulse.test',      '__PASSWORD_HASH__', 'admin'),
(2, 'Brian Otieno',       'reception.kisumu@zahanatipulse.test',  '__PASSWORD_HASH__', 'receptionist'),
(2, 'Dr. Mercy Awino',    'clinician.kisumu@zahanatipulse.test',  '__PASSWORD_HASH__', 'clinician'),
(2, 'Samuel Onyango',     'pharmacy.kisumu@zahanatipulse.test',   '__PASSWORD_HASH__', 'pharmacist');

INSERT INTO patients (facility_id, patient_number, full_name, date_of_birth, phone, created_by) VALUES
(1, 'MRU-0001', 'Mary Wanjiru',     '1990-03-14', '0700 000 101', 2),
(1, 'MRU-0002', 'John Mugambi',     '1985-07-22', '0700 000 102', 2),
(1, 'MRU-0003', 'Esther Kendi',     '2001-11-05', '0700 000 103', 2),
(1, 'MRU-0004', 'David Mutwiri',    '1978-01-30', '0700 000 104', 2),
(1, 'MRU-0005', 'Lucy Karimi',      '1995-09-18', '0700 000 105', 2),
(1, 'MRU-0006', 'Samuel Gitonga',   '2010-04-02', '0700 000 106', 2),
(2, 'KSM-0001', 'Rose Atieno',      '1988-02-11', '0700 000 201', 6),
(2, 'KSM-0002', 'Kevin Ochieng',    '1992-06-25', '0700 000 202', 6),
(2, 'KSM-0003', 'Beatrice Akinyi',  '1999-12-08', '0700 000 203', 6),
(2, 'KSM-0004', 'Dennis Omondi',    '1975-05-19', '0700 000 204', 6),
(2, 'KSM-0005', 'Joyce Adhiambo',   '1983-10-03', '0700 000 205', 6),
(2, 'KSM-0006', 'Collins Owino',    '2008-08-27', '0700 000 206', 6);

INSERT INTO appointments (facility_id, patient_id, appointment_datetime, service, status, created_by) VALUES
(1, 1, NOW() + INTERVAL '1 day',  'General Consultation', 'Scheduled', 2),
(1, 2, NOW() + INTERVAL '2 days', 'Follow-up',            'Scheduled', 2),
(1, 3, NOW() + INTERVAL '3 days', 'Antenatal Clinic',     'Scheduled', 2),
(1, 4, NOW() - INTERVAL '2 days', 'Laboratory',           'Completed', 2),
(2, 7, NOW() + INTERVAL '1 day',  'General Consultation', 'Scheduled', 6),
(2, 8, NOW() + INTERVAL '2 days', 'Follow-up',            'Scheduled', 6),
(2, 9, NOW() + INTERVAL '3 days', 'Antenatal Clinic',     'Scheduled', 6),
(2, 10, NOW() - INTERVAL '1 day', 'Laboratory',           'Cancelled', 6);

INSERT INTO queue_entries (facility_id, patient_id, appointment_id, queue_number, department, status, called_at, completed_at) VALUES
(1, 1,  1,    1, 'General', 'Completed',  NOW() - INTERVAL '40 minutes', NOW() - INTERVAL '20 minutes'),
(1, 5,  NULL, 2, 'General', 'In Service', NOW() - INTERVAL '10 minutes', NULL),
(1, 6,  NULL, 3, 'General', 'Waiting',    NULL, NULL),
(2, 7,  5,    1, 'General', 'Completed',  NOW() - INTERVAL '35 minutes', NOW() - INTERVAL '15 minutes'),
(2, 11, NULL, 2, 'General', 'Waiting',    NULL, NULL),
(2, 12, NULL, 3, 'General', 'Waiting',    NULL, NULL);

INSERT INTO medicines (name, strength, form) VALUES
('Paracetamol',                 '500 mg',      'Tablet'),
('Amoxicillin',                 '500 mg',      'Capsule'),
('Artemether/Lumefantrine',     '20/120 mg',   'Tablet'),
('Oral Rehydration Salts',      '20.5 g',      'Sachet'),
('Metformin',                   '500 mg',      'Tablet'),
('Amlodipine',                  '5 mg',        'Tablet'),
('Ibuprofen',                   '400 mg',      'Tablet'),
('Salbutamol',                  '100 mcg',     'Inhaler');

INSERT INTO inventory (facility_id, medicine_id, quantity, reorder_level) VALUES
(1, 1, 500, 100),
(1, 2,  40,  50),
(1, 3, 120,  30),
(1, 4,  15,  20),
(1, 5, 200,  40),
(1, 6,  80,  30),
(2, 1, 300, 100),
(2, 2,  90,  50),
(2, 3,  10,  30),
(2, 4,  60,  20),
(2, 5,  25,  40),
(2, 6, 150,  30);

INSERT INTO stock_movements (facility_id, inventory_id, user_id, movement_type, quantity_changed) VALUES
(1, 1, 4, 'received', 200),
(1, 2, 4, 'issued',    10),
(2, 7, 8, 'received', 100),
(2, 9, 8, 'issued',    20);