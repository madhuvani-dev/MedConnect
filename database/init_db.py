import sqlite3

def init_database():
    # 1. Connect to database file (creates database.db automatically if it doesn't exist)
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()

    # 2. Enable Foreign Key constraints in SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    #Admin table
    cursor.execute('''CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)''')



    #users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')

    # 3. Create Table 1: pharmacies
    cursor.execute('''
      CREATE TABLE IF NOT EXISTS pharmacies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shop_name TEXT NOT NULL,
    owner_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    phone TEXT NOT NULL,
    dl_number TEXT NOT NULL UNIQUE,
    address TEXT NOT NULL,
    status TEXT DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
    ''')

    # 4. Create Table 2: medicines
    cursor.execute('''
       CREATE TABLE IF NOT EXISTS medicines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    generic_name TEXT,
    manufacturer TEXT,
    category TEXT
    )
        
    ''')

    # 5. Create Table 3: inventory (Links pharmacy & medicine with availability status)
    cursor.execute('''
       CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pharmacy_id INTEGER NOT NULL,
    medicine_id INTEGER NOT NULL,
    availability_status INTEGER DEFAULT 1,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (pharmacy_id) REFERENCES pharmacies(id) ON DELETE CASCADE,
    FOREIGN KEY (medicine_id) REFERENCES medicines(id) ON DELETE CASCADE
    )
    ''')

    # 6. Insert Mock Seed Data for Phase 1 Demo
    # Adding a couple of initial pharmacies
    cursor.execute('''
        INSERT OR IGNORE INTO pharmacies
(id, shop_name, owner_name, email, password, phone, dl_number, address, status)
VALUES
(1, 'Apex Medical Stores', 'Ramesh Kumar', 'apex@example.com', 'password123', '+91 9123456789', 'DL-2026-TG1122', 'Hyderabad', 'Approved'),

(2, 'Relief Pharmacy & Surgical', 'Suresh Reddy', 'relief@example.com', 'password123', '+91 9876543210', 'DL-2026-TG3344', 'Warangal', 'Approved'),

(3, 'Quick Health Meds', 'Anil Rao', 'quick@example.com', 'password123', '+91 9000000000', 'PENDING-DL-9999', 'Karimnagar', 'Pending')
        
    ''')

    # Adding initial common medicines
    cursor.execute('''
        INSERT OR IGNORE INTO medicines (id, name, category) 
        VALUES 
        (1, 'Paracetamol', 'Fever & Pain Relief'),
        (2, 'Amoxicillin', 'Antibiotics'),
        (3, 'Augmentin', 'Antibiotics'),
        (4, 'ORS Sachet', 'Hydration')
    ''')

    # Adding initial inventory stock links
    cursor.execute('''
        INSERT OR IGNORE INTO inventory
(pharmacy_id, medicine_id, availability_status)
VALUES
(1, 1, 1),
(1, 3, 1),
(1, 4, 0),
(2, 1, 1),
(2, 2, 1)
    ''')

    # Save changes and close connection
    conn.commit()
    conn.close()
    print("✅ Success: database.db created with initial tables and mock data!")

if __name__ == '__main__':
    init_database()