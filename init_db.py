import sqlite3

def init_database():
    # 1. Connect to database file (creates database.db automatically if it doesn't exist)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # 2. Enable Foreign Key constraints in SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 3. Create Table 1: pharmacies
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pharmacies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dl_number TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            is_verified BOOLEAN DEFAULT 0
        )
    ''')

    # 4. Create Table 2: medicines
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            category TEXT
        )
    ''')

    # 5. Create Table 3: inventory (Links pharmacy & medicine with availability status)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pharmacy_id INTEGER NOT NULL,
            medicine_id INTEGER NOT NULL,
            is_available BOOLEAN DEFAULT 1,
            FOREIGN KEY (pharmacy_id) REFERENCES pharmacies (id) ON DELETE CASCADE,
            FOREIGN KEY (medicine_id) REFERENCES medicines (id) ON DELETE CASCADE
        )
    ''')

    # 6. Insert Mock Seed Data for Phase 1 Demo
    # Adding a couple of initial pharmacies
    cursor.execute('''
        INSERT OR IGNORE INTO pharmacies (id, name, dl_number, phone, is_verified) 
        VALUES 
        (1, 'Apex Medical Stores', 'DL-2026-TG1122', '+91 9123456789', 1),
        (2, 'Relief Pharmacy & Surgical', 'DL-2026-TG3344', '+91 9876543210', 1),
        (3, 'Quick Health Meds', 'PENDING-DL-9999', '+91 9000000000', 0)
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
        INSERT OR IGNORE INTO inventory (pharmacy_id, medicine_id, is_available) 
        VALUES 
        (1, 1, 1), -- Apex has Paracetamol (In Stock)
        (1, 3, 1), -- Apex has Augmentin (In Stock)
        (1, 4, 0), -- Apex has ORS Sachet (Out of Stock)
        (2, 1, 1), -- Relief has Paracetamol (In Stock)
        (2, 2, 1)  -- Relief has Amoxicillin (In Stock)
    ''')

    # Save changes and close connection
    conn.commit()
    conn.close()
    print("✅ Success: database.db created with initial tables and mock data!")

if __name__ == '__main__':
    init_database()