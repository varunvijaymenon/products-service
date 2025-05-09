import json
from typing import List
from app.models import Product
from pathlib import Path

DATA_FILE = Path(__file__).parent / "products.json"

# Load initial products from JSON
def load_products_from_json(filepath: Path = DATA_FILE) -> List[Product]:
    if not filepath.exists():
        return []
    with open(filepath, "r") as f:
        data = json.load(f)
        return [Product(**item) for item in data]

# Save current products to JSON
def save_products_to_json(products: List[Product], filepath: Path = DATA_FILE):
    with open(filepath, "w") as f:
        json.dump([product.dict() for product in products], f, indent=4)

# Initialize product list
products_db: List[Product] = load_products_from_json(DATA_FILE)
# print(products_db)
