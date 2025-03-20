import sqlite3

DB_PATH = r"C:\Users\cdm1\OneDrive - University of Tasmania\Documents\tasmanian_seasons\tasmania_ecology.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Add new columns if they don't exist
cursor.execute("ALTER TABLE plants ADD COLUMN habitat TEXT DEFAULT ''")
cursor.execute("ALTER TABLE plants ADD COLUMN flowering_period TEXT DEFAULT ''")
cursor.execute("ALTER TABLE plants ADD COLUMN notes TEXT DEFAULT ''")
cursor.execute("ALTER TABLE plants ADD COLUMN completed INTEGER DEFAULT 0")

conn.commit()
conn.close()

print("Database updated with additional fields and completion flag.")
