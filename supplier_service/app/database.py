import json
from typing import List
from app.models import Supplier
from pathlib import Path

DATA_FILE = Path(__file__).parent / "suppliers.json"

# Load initial suppliers from JSON
def load_suppliers_from_json(filepath: Path = DATA_FILE) -> List[Supplier]:
    if not filepath.exists():
        return []
    with open(filepath, "r") as f:
        data = json.load(f)
        return [Supplier(**item) for item in data]

# Save current suppliers to JSON
def save_suppliers_to_json(suppliers: List[Supplier], filepath: Path = DATA_FILE):
    with open(filepath, "w") as f:
        json.dump([supplier.dict() for supplier in suppliers], f, indent=4)

# Initialize supplier list
suppliers_db: List[Supplier] = load_suppliers_from_json(DATA_FILE)
# print(suppliers_db)