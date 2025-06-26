import os, random
from dotenv import load_dotenv
from faker import Faker
from sqlalchemy.orm import Session
from database import SessionLocal
from Users.models import User
from sqlalchemy import insert
 
load_dotenv()
fake = Faker()
 
GENDERS = ["male", "female", "other"]
NATIONALITIES = ["Indian", "American", "British", "German", "French", "Japanese", "Canadian"]
 
def generate_user_dict():
    suffix = random.randint(1, 99999)
    local, domain = fake.unique.email().split("@")
    raw_phone = fake.phone_number()
    phone = raw_phone[:50]  
    return {
        "username": fake.user_name(),
        "email": f"{local}{suffix}@{domain}",
        "password": fake.password(length=10),  
        "gender": random.choice(GENDERS),
        "age": random.randint(18, 65),
        "phone_number": phone,
        "nationality": random.choice(NATIONALITIES),
        "is_active": random.choice([True, False])
    }
 
def filter_batch(batch):
    seen_u, seen_e = set(), set()
    unique = []
    for r in batch:
        if r["username"] in seen_u or r["email"] in seen_e:
            continue
        seen_u.add(r["username"])
        seen_e.add(r["email"])
        unique.append(r)
    return unique
 
def main(total=50000, chunk_size=1000):
    db: Session = SessionLocal()
    count = 0
    for i in range(0, total, chunk_size):
        batch = [generate_user_dict() for _ in range(min(chunk_size, total - i))]
        batch = filter_batch(batch)
        if not batch:
            continue
        try:
            stmt = insert(User.__table__).prefix_with("IGNORE")
            db.execute(stmt, batch)
            db.commit()
            count += len(batch)
            if count % 1000 == 0:
                print(f"✅ Inserted {count}/{total} users")
        except Exception as e:
            db.rollback()
            print(f"❌ Error inserting batch starting at {i + 1}: {e}")
    db.close()
    print(f"🎉 Completed inserting {count}/{total} users")
 
if __name__ == "__main__":
    main()