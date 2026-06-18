import os
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

def seed_db():
    db = SessionLocal()
    try:
        # Create tables if not exist
        models.Base.metadata.create_all(bind=engine)
        
        # Clear existing data to ensure exactly 29 fresh entries
        print("Clearing existing database tables...")
        db.query(models.OrderItem).delete()
        db.query(models.Order).delete()
        db.query(models.Product).delete()
        db.query(models.Customer).delete()
        db.commit()

        print("Seeding 29 Indian products...")
        products_data = [
            ("Premium Basmati Rice (5kg)", "PROD-BSR-01", 14.99, 120),
            ("Organic Turmeric Powder (250g)", "PROD-TRM-02", 3.49, 200),
            ("Masala Chai CTC Tea (1kg)", "PROD-MCT-03", 9.99, 85),
            ("Cold Pressed Coconut Oil (1L)", "PROD-CNO-04", 12.50, 60),
            ("Kashmiri Red Chilli (100g)", "PROD-KRC-05", 2.99, 150),
            ("Pure Cow Ghee (1L)", "PROD-GHE-06", 18.00, 45),
            ("Tamarind Paste (400g)", "PROD-TAM-07", 3.99, 90),
            ("Alphonso Mango Pulp (850g)", "PROD-AMP-08", 6.49, 8), # Low stock
            ("Chana Masala Spice Mix", "PROD-CMS-09", 1.99, 110),
            ("Whole Garam Masala (200g)", "PROD-GMS-10", 4.99, 70),
            ("Premium Cashew Nuts (500g)", "PROD-CAS-11", 11.99, 50),
            ("California Almonds (500g)", "PROD-ALM-12", 9.99, 3), # Low stock
            ("Green Cardamom (50g)", "PROD-CRD-13", 5.99, 80),
            ("Handcrafted Copper Bottle", "PROD-CPB-14", 24.99, 35),
            ("Eco-friendly Yoga Mat", "PROD-YGM-15", 19.99, 15),
            ("Darjeeling Green Tea (250g)", "PROD-DGT-16", 8.49, 0), # Out of stock
            ("Pure Wild Forest Honey (500g)", "PROD-HON-17", 7.99, 55),
            ("Whole Wheat Chakki Atta (10kg)", "PROD-ATT-18", 16.99, 95),
            ("Premium Moong Dal (1kg)", "PROD-MNG-19", 3.80, 140),
            ("Sona Masoori Rice (10kg)", "PROD-SMR-20", 22.99, 4), # Low stock
            ("Organic Jaggery Powder (1kg)", "PROD-JAG-21", 4.50, 65),
            ("Natural Henna Powder (200g)", "PROD-HEN-22", 3.25, 120),
            ("Ayurvedic Ashwagandha (60 caps)", "PROD-ASH-23", 14.50, 40),
            ("Triphala Herbal Tablets", "PROD-TRI-24", 11.00, 30),
            ("Neem Soap Pack of 3", "PROD-NEM-25", 5.99, 90),
            ("Sandalwood Incense Sticks", "PROD-INC-26", 2.49, 180),
            ("Handwoven Cotton Table Runner", "PROD-CTR-27", 15.99, 25),
            ("Traditional Clay Diya (Set of 6)", "PROD-DIY-28", 4.99, 0), # Out of stock
            ("Amritsari Wari (500g)", "PROD-WAR-29", 5.49, 42)
        ]
        
        products = [
            models.Product(name=p[0], sku=p[1], price=p[2], quantity=p[3])
            for p in products_data
        ]
        db.add_all(products)

        print("Seeding 29 Indian customers...")
        customers_data = [
            ("Aarav Sharma", "aarav.sharma@example.in", "+919876543210"),
            ("Ananya Patel", "ananya.patel@example.in", "+919812345678"),
            ("Vihaan Gupta", "vihaan.gupta@example.in", "+919922334455"),
            ("Diya Iyer", "diya.iyer@example.in", "+919011223344"),
            ("Arjun Verma", "arjun.verma@example.in", "+919555667788"),
            ("Saisha Reddy", "saisha.reddy@example.in", "+919666778899"),
            ("Aditya Nair", "aditya.nair@example.in", "+919777889900"),
            ("Ishaan Joshi", "ishaan.joshi@example.in", "+919888990011"),
            ("Kiara Rao", "kiara.rao@example.in", "+919999001122"),
            ("Sai Prasad", "sai.prasad@example.in", "+919111223344"),
            ("Rohan Deshmukh", "rohan.deshmukh@example.in", "+919222334455"),
            ("Riya Sen", "riya.sen@example.in", "+919333445566"),
            ("Kabir Singh", "kabir.singh@example.in", "+919444556677"),
            ("Myra Kapoor", "myra.kapoor@example.in", "+919555667788"),
            ("Reyansh Gill", "reyansh.gill@example.in", "+919666778899"),
            ("Anika Roy", "anika.roy@example.in", "+919777889900"),
            ("Dev Choudhury", "dev.choudhury@example.in", "+919888990011"),
            ("Samaira Dutta", "samaira.dutta@example.in", "+919999001122"),
            ("Atharv Saxena", "atharv.saxena@example.in", "+919000112233"),
            ("Shruti Mishra", "shruti.mishra@example.in", "+919111002233"),
            ("Kian Malhotra", "kian.malhotra@example.in", "+919222003344"),
            ("Zara Khan", "zara.khan@example.in", "+919333004455"),
            ("Aanya Trivedi", "aanya.trivedi@example.in", "+919444005566"),
            ("Krishna Bhat", "krishna.bhat@example.in", "+919555006677"),
            ("Avani Hegde", "avani.hegde@example.in", "+919666007788"),
            ("Yuvan Banerjee", "yuvan.banerjee@example.in", "+919777008899"),
            ("Meera Joshi", "meera.joshi@example.in", "+919888009900"),
            ("Ranbir Kapoor", "ranbir.kapoor@example.in", "+919999000011"),
            ("Pooja Hegde", "pooja.hegde@example.in", "+919000223311")
        ]

        customers = [
            models.Customer(name=c[0], email=c[1], phone=c[2])
            for c in customers_data
        ]
        db.add_all(customers)
        
        db.commit()
        print("✅ Database successfully seeded with 29 Indian customers and products!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
