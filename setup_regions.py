import sqlite3

DB_PATH = r"C:\Users\cdm1\OneDrive - University of Tasmania\Documents\tasmanian_seasons\tasmania_ecology.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Add columns if they don't exist
cursor.execute("ALTER TABLE plants ADD COLUMN biogeographic_regions TEXT DEFAULT ''")

conn.commit()
conn.close()

print("Database updated with biogeographic regions.")
