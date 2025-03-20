import sqlite3

# Database path
DB_PATH = r"C:\Users\cdm1\OneDrive - University of Tasmania\Documents\tasmanian_seasons\tasmania_ecology.db"

# Connect to the database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create the plant_edits table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS plant_edits (
        edit_id INTEGER PRIMARY KEY AUTOINCREMENT,
        plant_id INTEGER,
        field_name TEXT,
        old_value TEXT,
        new_value TEXT,
        edit_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (plant_id) REFERENCES plants (plant_id) ON DELETE CASCADE
    )
""")

conn.commit()
conn.close()

print("Table 'plant_edits' has been created successfully.")
