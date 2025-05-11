import json
from typing import List
from app.models import Order
from pathlib import Path

DATA_FILE = Path(__file__).parent / "orders.json"

# Load initial orders from JSON
def load_orders_from_json(filepath: Path = DATA_FILE) -> List[Order]:
    if not filepath.exists():
        return []
    with open(filepath, "r") as f:
        data = json.load(f)
        return [Order(**item) for item in data]

# Save current products to JSON
def save_orders_to_json(orders: List[Order], filepath: Path = DATA_FILE):
    with open(filepath, "w") as f:
        json.dump([order.dict() for order in orders], f, indent=4)

# Initialize product list
orders_db: List[Order] = load_orders_from_json(DATA_FILE)
# print(orders_db)
