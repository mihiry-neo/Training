import random
from typing import List, Dict, Any
from faker import Faker
from sqlalchemy.orm import Session
from models import Product, Category, PriceHistory

class DataGenerator:
    def __init__(self):
        self.faker = Faker()
        self.global_categories = [
            "Fashion", "Electronics", "Home & Garden", "Food & Beverage",
            "Health & Beauty", "Books & Media", "Toys & Games",
            "Sports & Outdoors", "DIY & Hardware", "Furniture"
        ]
        self.category_subcategories = {
            "Fashion": ["Clothing", "Footwear", "Accessories"],
            "Electronics": ["Mobiles", "Laptops", "Appliances"],
            "Home & Garden": ["Decor", "Plants", "Kitchen"],
            "Food & Beverage": ["Snacks", "Drinks", "Groceries"],
            "Health & Beauty": ["Skincare", "Supplements", "Makeup"],
            "Books & Media": ["Books", "Magazines", "E-books"],
            "Toys & Games": ["Board Games", "Action Figures", "Educational"],
            "Sports & Outdoors": ["Fitness", "Cycling", "Camping"],
            "DIY & Hardware": ["Tools", "Paint", "Electrical"],
            "Furniture": ["Bedroom", "Office", "Living Room"]
        }

        self.brand_names = [
            "Astra", "Zenex", "Nova", "UrbanMode", "GearPro",
            "CraftHaus", "NextEra", "Skyline", "PureEssence", "Flytek"
        ]

    def create_categories(self, db: Session) -> List[Category]:
        categories = []
        for main_name in self.global_categories:
            main_cat = Category(name=main_name)
            db.add(main_cat)
            db.flush()
            categories.append(main_cat)

            sub_names = self.category_subcategories.get(main_name, [])
            for sub in sub_names:
                sub_cat = Category(name=f"{main_name} - {sub}", parent_id=main_cat.id)
                db.add(sub_cat)
                db.flush()
                categories.append(sub_cat)

        db.commit()
        return categories


    def generate_brand(self) -> str:
        return random.choice([
            random.choice(self.brand_names),
            f"{self.faker.last_name()} {random.choice(['Inc', 'Corp', 'Ltd', 'Group'])}",
            f"{self.faker.country_code()} Tech",
            f"{self.faker.word().capitalize()}Works"
        ])

    def generate_product_attributes(self, category_name: str) -> Dict[str, Any]:
        return {
            "color": self.faker.color_name(),
            "weight": (
                f"{random.uniform(0.2, 3.0):.2f} kg"
                if "Electronics" in category_name or "Toys" in category_name
                else f"{random.uniform(5.0, 50.0):.2f} kg"
                if "Furniture" in category_name
                else f"{random.uniform(0.5, 10.0):.2f} kg"
            ),
            "material": (
                random.choice(["Cotton", "Polyester", "Denim", "Wool", "Silk"])
                if "Fashion" in category_name
                else random.choice(["Wood", "Metal", "Glass", "Plastic", "Leather"])
                if "Furniture" in category_name
                else random.choice(["Plastic", "Aluminum", "Glass"])
            ),
            "rating": round(random.uniform(3.0, 5.0), 1)
        }

    def generate_product(self, categories: List[Category]) -> Dict[str, Any]:
        category = random.choice(categories)
        return {
            "name": f"{self.faker.word().capitalize()} {self.faker.word().capitalize()}",
            "price": round(
                random.uniform(200.0, 2000.0)
                if "Electronics" in category.name or "Furniture" in category.name
                else random.uniform(50.0, 500.0)
                if "Fashion" in category.name
                else random.uniform(10.0, 300.0),
                2
            ),
            "category_id": category.id,
            "brand": self.generate_brand(),
            "stock_quantity": random.randint(0, 1000),
            "attributes": self.generate_product_attributes(category.name)
        }

    def create_products(self, db: Session, categories: List[Category], count: int = 100) -> List[Product]:
        products = []
        for _ in range(count):
            product_data = self.generate_product(categories)
            product = Product(**product_data)
            db.add(product)
            products.append(product)

        db.commit()
        return products

    def update_product_price(self, db: Session, product: Product, reason: str = "random_update") -> None:
        old_price = product.price
        change_percent = random.uniform(-0.2, 0.2)
        new_price = round(old_price * (1 + change_percent), 2)
        new_price = max(new_price, 1.0)

        price_history = PriceHistory(
            product_id=product.id,
            old_price=old_price,
            new_price=new_price,
            reason=reason
        )

        product.price = new_price
        db.add(price_history)
        db.commit()

    def update_stock_quantity(self, db: Session, product: Product) -> None:
        change = random.randint(-50, 100)
        new_quantity = max(0, product.stock_quantity + change)
        product.stock_quantity = new_quantity
        db.commit()

    def generate_new_product(self, db: Session, categories: List[Category]) -> Product:
        product_data = self.generate_product(categories)
        product = Product(**product_data)
        db.add(product)
        db.commit()
        return product
