import sqlite3
import os

# Define database filename
db_filename = "tasmania_ecology.db"

# Ensure the file is created
if not os.path.exists(db_filename):
    open(db_filename, 'w').close()

# Connect to (or create) the database file
conn = sqlite3.connect(db_filename)
cursor = conn.cursor()

# Create Plants table
cursor.execute("""
CREATE TABLE IF NOT EXISTS plants (
    plant_id INTEGER PRIMARY KEY AUTOINCREMENT,
    scientific_name TEXT UNIQUE NOT NULL,
    common_name TEXT,
    family TEXT,
    genus TEXT,
    region TEXT,
    habitat_type TEXT
)
""")

# Create Flowering Observations table
cursor.execute("""
CREATE TABLE IF NOT EXISTS flowering_observations (
    observation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    plant_id INTEGER,
    location TEXT,
    date_recorded TEXT,
    observer TEXT,
    flowering_stage TEXT,
    reference TEXT,
    FOREIGN KEY (plant_id) REFERENCES plants (plant_id) ON DELETE CASCADE
)
""")

# Create Climate Data table
cursor.execute("""
CREATE TABLE IF NOT EXISTS climate_data (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    location TEXT,
    temperature REAL,
    rainfall REAL,
    other_factors TEXT
)
""")

# Create Phenology Trends table
cursor.execute("""
CREATE TABLE IF NOT EXISTS phenology_trends (
    trend_id INTEGER PRIMARY KEY AUTOINCREMENT,
    plant_id INTEGER,
    region TEXT,
    avg_first_flowering TEXT,
    avg_peak_flowering TEXT,
    trend_over_time TEXT,
    FOREIGN KEY (plant_id) REFERENCES plants (plant_id) ON DELETE CASCADE
)
""")

# Commit and close connection
conn.commit()
conn.close()

print(f"Database '{db_filename}' has been created successfully.")
