# generate_all_data.py

from genusers import main as generate_users
from genpro import main as generate_products
from genorders import main as generate_orders

def generate_all_data_pipeline():
    print("🚀 Generating USERS...")
    generate_users(500)  # updated: positional argument only

    print("📦 Generating PRODUCTS...")
    generate_products(200)  # updated: positional argument only

    print("🛒 Generating ORDERS...")
    generate_orders()

    print("✅ Data generation complete.")

if __name__ == "__main__":
    generate_all_data_pipeline()
