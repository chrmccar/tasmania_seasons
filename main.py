import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
    QTextEdit, QFormLayout, QMessageBox, QListWidget, QCheckBox, QGridLayout, QGroupBox
)

# Database path
DB_PATH = r"C:\Users\cdm1\OneDrive - University of Tasmania\Documents\tasmanian_seasons\tasmania_ecology.db"

# Habitat options
HABITATS = [
    "Dry eucalypt forest and woodland", "Highland and treeless vegetation", "Modified land",
    "Moorland, sedgeland and rushland", "Native grassland", "Non eucalypt forest and woodland",
    "Other natural environments", "Rainforest and related scrub", "Saltmarsh and wetland",
    "Scrub and heathland and coastal complexes", "Wet eucalypt forest and woodland"
]

# Biogeographic Regions options
BIOREGIONS = [
    "King", "Tasmanian Northern Slopes", "Tasmanian Central Highlands", "Tasmanian West",
    "Tasmanian Southern Ranges", "Tasmanian South East", "Tasmanian Northern Midlands",
    "Ben Lomond", "Furneaux"
]

class PlantDatabaseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tasmania Plant Database")
        self.setGeometry(100, 100, 900, 800)  # Increased window size

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        container = QWidget()
        container.setLayout(layout)
        scroll_area.setWidget(container)

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        # Main Layout
        layout = QVBoxLayout()
        
        # Search Section
        self.search_label = QLabel("Search for a species:")
        layout.addWidget(self.search_label)

        self.search_input = QLineEdit()
        layout.addWidget(self.search_input)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_species)
        layout.addWidget(self.search_button)

        self.results_list = QListWidget()
        layout.addWidget(self.results_list, 1)

        # Species Details
        self.details_label = QLabel("Edit Species Details:")
        layout.addWidget(self.details_label)

        form_layout = QFormLayout()
        self.genus_input = QLineEdit()
        self.clade_input = QLineEdit()
        self.taxonomy_status_input = QLineEdit()
        self.citation_input = QTextEdit()
        self.citation_input.setMaximumHeight(50)  # Limit height

        self.flowering_input = QLineEdit()
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(50)  # Limit height
        self.completed_checkbox = QCheckBox("Mark as Completed")

        form_layout.addRow("Genus:", self.genus_input)
        form_layout.addRow("Clade:", self.clade_input)
        form_layout.addRow("Taxonomy Status:", self.taxonomy_status_input)
        form_layout.addRow("Citation:", self.citation_input)
        form_layout.addRow("Flowering Period:", self.flowering_input)
        form_layout.addRow("Notes:", self.notes_input)
        form_layout.addRow("", self.completed_checkbox)

        layout.addLayout(form_layout)

        # Habitat Selection
        self.habitat_group = QGroupBox("Select Habitat(s):")
        habitat_layout = QVBoxLayout()
        self.habitat_checkboxes = {}
        for habitat in HABITATS:
            checkbox = QCheckBox(habitat)
            self.habitat_checkboxes[habitat] = checkbox
            habitat_layout.addWidget(checkbox)
        self.habitat_group.setLayout(habitat_layout)
        layout.addWidget(self.habitat_group)

        # Biogeographic Regions Selection
        self.bioregion_group = QGroupBox("Select Biogeographic Region(s):")
        bioregion_layout = QVBoxLayout()
        self.bioregion_checkboxes = {}
        for region in BIOREGIONS:
            checkbox = QCheckBox(region)
            self.bioregion_checkboxes[region] = checkbox
            bioregion_layout.addWidget(checkbox)
        self.bioregion_group.setLayout(bioregion_layout)
        layout.addWidget(self.bioregion_group)

        # Buttons
        self.save_button = QPushButton("Save Changes")
        self.save_button.setMinimumHeight(40)  # Bigger button
        self.save_button.clicked.connect(self.save_changes)
        layout.addWidget(self.save_button)

        self.history_button = QPushButton("View Edit History")
        self.history_button.setMinimumHeight(40)  # Bigger button
        self.history_button.clicked.connect(self.view_edit_history)
        layout.addWidget(self.history_button)

        # Edit History Display
        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)
        self.history_text.setMaximumHeight(100)  # Limit height
        layout.addWidget(self.history_text)

        self.setLayout(layout)


    def search_species(self):
        search_text = self.search_input.text().strip().lower()
        if not search_text:
            QMessageBox.warning(self, "Error", "Please enter a search term.")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT plant_id, scientific_name FROM plants WHERE LOWER(scientific_name) LIKE ?", 
                       (f"%{search_text}%",))
        results = cursor.fetchall()
        conn.close()

        self.results_list.clear()
        if results:
            for row in results:
                self.results_list.addItem(f"{row[0]} - {row[1]}")
        else:
            self.results_list.addItem("No results found.")

    def load_species_details(self, item):
        selected_text = item.text()
        plant_id = selected_text.split(" - ")[0]
        self.current_plant_id = plant_id

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT genus, clade, taxonomy_status, citation, flowering_period, notes, completed, habitat, biogeographic_regions
            FROM plants WHERE plant_id = ?
        """, (plant_id,))
        result = cursor.fetchone()
        conn.close()

        if result:
            self.genus_input.setText(result[0] or "")
            self.clade_input.setText(result[1] or "")
            self.taxonomy_status_input.setText(result[2] or "")
            self.citation_input.setText(result[3] or "")
            self.flowering_input.setText(result[4] or "")
            self.notes_input.setText(result[5] or "")
            self.completed_checkbox.setChecked(result[6] == 1)

            for habitat in HABITATS:
                self.habitat_checkboxes[habitat].setChecked(habitat in (result[7] or ""))

            for region in BIOREGIONS:
                self.bioregion_checkboxes[region].setChecked(region in (result[8] or ""))

    def save_changes(self):
        if not self.current_plant_id:
            QMessageBox.warning(self, "Error", "No species selected.")
            return

        new_habitat = ",".join([h for h in HABITATS if self.habitat_checkboxes[h].isChecked()])
        new_bioregions = ",".join([r for r in BIOREGIONS if self.bioregion_checkboxes[r].isChecked()])
        new_completed = 1 if self.completed_checkbox.isChecked() else 0

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE plants SET habitat = ?, biogeographic_regions = ?, completed = ?
            WHERE plant_id = ?
        """, (new_habitat, new_bioregions, new_completed, self.current_plant_id))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Changes saved successfully.")

    def view_edit_history(self):
        """Display edit history for the selected species."""
        if not self.current_plant_id:
            QMessageBox.warning(self, "Error", "No species selected.")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT field_name, old_value, new_value, edit_timestamp 
            FROM plant_edits WHERE plant_id = ? ORDER BY edit_timestamp DESC
        """, (self.current_plant_id,))
        results = cursor.fetchall()
        conn.close()

        history_text = "\n".join(
            [f"{row[3]}: {row[0]} changed from '{row[1]}' to '{row[2]}'" for row in results]
        ) if results else "No edit history available."

        self.history_text.setText(history_text)


# Run the Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlantDatabaseApp()
    window.show()
    sys.exit(app.exec_())
