import json
import os


def load_products():
    """Load products list from products.json (handles top-level 'products' key)."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "products.json")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "products" in data:
        return data["products"]
    return data


def get_categories(products):
    return sorted(set(p["category"] for p in products))


def get_brands(products):
    return sorted(set(p["brand"] for p in products))


def filter_products(products, search_query="", category="All",
                    min_price=0, max_price=5000, min_rating=0.0):
    filtered = products

    if search_query:
        q = search_query.lower()
        filtered = [
            p for p in filtered
            if q in p["name"].lower()
            or q in p["brand"].lower()
            or q in p["category"].lower()
            or any(q in tag.lower() for tag in p.get("tags", []))
        ]

    if category and category != "All":
        filtered = [p for p in filtered if p["category"] == category]

    filtered = [p for p in filtered if min_price <= p["price"] <= max_price]
    filtered = [p for p in filtered if p["rating"] >= min_rating]

    return filtered


def get_recommendations(products, current_product, n=3):
    same_cat = [p for p in products
                if p["category"] == current_product["category"]
                and p["id"] != current_product["id"]]
    scored = sorted(
        same_cat,
        key=lambda p: len(set(p.get("tags", [])) & set(current_product.get("tags", []))),
        reverse=True,
    )
    return scored[:n]
