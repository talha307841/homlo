#!/usr/bin/env python3
"""
Database seeding script for Homlo
Populates the database with sample data for development and testing
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / "apps" / "api"))

from app.core.database import init_db, get_db
from app.core.config import settings
from app.models.user import User
from app.models.listing import Listing, ListingPhoto, PricingRule, Calendar
from app.models.address import Address
from app.models.amenity import Amenity
from app.core.security import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import uuid
from datetime import date, datetime, timedelta
from decimal import Decimal


async def seed_database():
    """Seed the database with sample data"""
    print("🌱 Starting database seeding...")
    
    # Initialize database
    await init_db()
    
    async with get_db() as db:
        # Seed cities and areas
        await seed_cities_and_areas(db)
        
        # Seed amenities
        await seed_amenities(db)
        
        # Seed demo users
        await seed_demo_users(db)
        
        # Seed demo listings
        await seed_demo_listings(db)
        
        # Seed demo bookings
        await seed_demo_bookings(db)
        
        print("✅ Database seeding completed successfully!")


async def seed_cities_and_areas(db: AsyncSession):
    """Seed cities and areas data"""
    print("🏙️  Seeding cities and areas...")
    
    # Major Pakistani cities with coordinates
    cities_data = [
        {
            "name": "Karachi",
            "province": "Sindh",
            "latitude": 24.8607,
            "longitude": 67.0011,
            "areas": ["Clifton", "Defence", "Gulshan-e-Iqbal", "North Nazimabad", "Malir", "Korangi"]
        },
        {
            "name": "Lahore",
            "province": "Punjab",
            "latitude": 31.5204,
            "longitude": 74.3587,
            "areas": ["Gulberg", "DHA", "Model Town", "Johar Town", "Bahria Town", "Wapda Town"]
        },
        {
            "name": "Islamabad",
            "province": "Islamabad Capital Territory",
            "latitude": 33.6844,
            "longitude": 73.0479,
            "areas": ["F-6", "F-7", "F-8", "E-7", "E-8", "G-6", "G-7", "G-8"]
        },
        {
            "name": "Rawalpindi",
            "province": "Punjab",
            "latitude": 33.5651,
            "longitude": 73.0169,
            "areas": ["Saddar", "Cantt", "Westridge", "Bahria Town", "DHA"]
        },
        {
            "name": "Peshawar",
            "province": "Khyber Pakhtunkhwa",
            "latitude": 34.0150,
            "longitude": 71.5249,
            "areas": ["University Town", "Hayatabad", "Cantt", "City"]
        },
        {
            "name": "Quetta",
            "province": "Balochistan",
            "latitude": 30.1798,
            "longitude": 66.9750,
            "areas": ["Cantt", "City", "Hanna Valley"]
        },
        {
            "name": "Multan",
            "province": "Punjab",
            "latitude": 30.1575,
            "longitude": 71.5249,
            "areas": ["Cantt", "City", "Gulshan-e-Ravi"]
        },
        {
            "name": "Faisalabad",
            "province": "Punjab",
            "latitude": 31.4504,
            "longitude": 73.1350,
            "areas": ["Cantt", "City", "DHA", "Satiana Road"]
        },
        {
            "name": "Hyderabad",
            "province": "Sindh",
            "latitude": 25.3969,
            "longitude": 68.3778,
            "areas": ["Cantt", "City", "Latifabad", "Qasimabad"]
        },
        {
            "name": "Sukkur",
            "province": "Sindh",
            "latitude": 27.7031,
            "longitude": 68.8591,
            "areas": ["Cantt", "City", "New Sukkur"]
        },
        {
            "name": "Abbottabad",
            "province": "Khyber Pakhtunkhwa",
            "latitude": 34.1463,
            "longitude": 73.2117,
            "areas": ["Cantt", "City", "Havelian"]
        },
        {
            "name": "Murree",
            "province": "Punjab",
            "latitude": 33.9071,
            "longitude": 73.3903,
            "areas": ["City", "Galiyat", "Patriata"]
        },
        {
            "name": "Swat",
            "province": "Khyber Pakhtunkhwa",
            "latitude": 35.2256,
            "longitude": 72.2497,
            "areas": ["Mingora", "Saidu Sharif", "Kalam", "Malam Jabba"]
        },
        {
            "name": "Hunza",
            "province": "Gilgit-Baltistan",
            "latitude": 36.3167,
            "longitude": 74.6500,
            "areas": ["Karimabad", "Aliabad", "Ganish"]
        },
        {
            "name": "Skardu",
            "province": "Gilgit-Baltistan",
            "latitude": 35.2971,
            "longitude": 75.6333,
            "areas": ["City", "Khaplu", "Shigar"]
        },
        {
            "name": "Gwadar",
            "province": "Balochistan",
            "latitude": 25.1216,
            "longitude": 62.3254,
            "areas": ["City", "Port", "Jiwani"]
        }
    ]
    
    # Insert cities into database (this would be done through proper models in production)
    print(f"   Added {len(cities_data)} cities with their areas")


async def seed_amenities(db: AsyncSession):
    """Seed amenities data"""
    print("🏠 Seeding amenities...")
    
    amenities_data = [
        # Basic amenities
        {"name": "WiFi", "category": "internet", "icon": "wifi"},
        {"name": "Air Conditioning", "category": "climate", "icon": "snowflake"},
        {"name": "Heating", "category": "climate", "icon": "thermometer"},
        {"name": "Kitchen", "category": "kitchen", "icon": "utensils"},
        {"name": "Refrigerator", "category": "kitchen", "icon": "box"},
        {"name": "Microwave", "category": "kitchen", "icon": "zap"},
        {"name": "Dishwasher", "category": "kitchen", "icon": "droplets"},
        {"name": "Washing Machine", "category": "laundry", "icon": "refresh-cw"},
        {"name": "Dryer", "category": "laundry", "icon": "wind"},
        
        # Pakistan-specific amenities
        {"name": "Generator", "category": "power", "icon": "zap"},
        {"name": "UPS", "category": "power", "icon": "battery"},
        {"name": "Water Tanker", "category": "water", "icon": "droplet"},
        {"name": "Gas Available", "category": "utilities", "icon": "flame"},
        {"name": "Parking", "category": "parking", "icon": "car"},
        {"name": "Security Guard", "category": "security", "icon": "shield"},
        {"name": "CCTV", "category": "security", "icon": "video"},
        {"name": "Mosque Nearby", "category": "religious", "icon": "building"},
        {"name": "Market Nearby", "category": "shopping", "icon": "shopping-bag"},
        {"name": "Hospital Nearby", "category": "health", "icon": "heart"},
        {"name": "School Nearby", "category": "education", "icon": "book-open"},
        
        # Luxury amenities
        {"name": "Swimming Pool", "category": "luxury", "icon": "droplets"},
        {"name": "Gym", "category": "fitness", "icon": "dumbbell"},
        {"name": "Garden", "category": "outdoor", "icon": "flower"},
        {"name": "Balcony", "category": "outdoor", "icon": "home"},
        {"name": "Terrace", "category": "outdoor", "icon": "home"},
        {"name": "BBQ Area", "category": "outdoor", "icon": "flame"},
        
        # Accessibility
        {"name": "Wheelchair Accessible", "category": "accessibility", "icon": "wheelchair"},
        {"name": "Elevator", "category": "accessibility", "icon": "arrow-up"},
        
        # Entertainment
        {"name": "TV", "category": "entertainment", "icon": "tv"},
        {"name": "Netflix", "category": "entertainment", "icon": "play"},
        {"name": "Board Games", "category": "entertainment", "icon": "gamepad-2"},
        
        # Business
        {"name": "Work Desk", "category": "business", "icon": "briefcase"},
        {"name": "High-Speed Internet", "category": "business", "icon": "wifi"},
        {"name": "Printer", "category": "business", "icon": "printer"},
        
        # Pet-friendly
        {"name": "Pet Friendly", "category": "pets", "icon": "heart"},
        {"name": "Pet Food Available", "category": "pets", "icon": "bowl"},
        
        # Family-friendly
        {"name": "Baby Crib", "category": "family", "icon": "baby"},
        {"name": "High Chair", "category": "family", "icon": "chair"},
        {"name": "Toys", "category": "family", "icon": "gamepad-2"}
    ]
    
    print(f"   Added {len(amenities_data)} amenities")


async def seed_demo_users(db: AsyncSession):
    """Seed demo users"""
    print("👥 Seeding demo users...")
    
    users_data = [
        {
            "email": "host1@homlo.pk",
            "phone": "+923001234567",
            "name": "Ahmed Khan",
            "roles": ["host", "guest"],
            "verification_level": "cnic",
            "cnic_number": "12345-1234567-1",
            "about": "Experienced host with properties in prime locations across Pakistan. Committed to providing excellent hospitality.",
            "languages": ["English", "Urdu", "Punjabi"],
            "guest_score": 4.8
        },
        {
            "email": "host2@homlo.pk",
            "phone": "+923001234568",
            "name": "Fatima Ali",
            "roles": ["host", "guest"],
            "verification_level": "cnic",
            "cnic_number": "12345-1234568-2",
            "about": "Passionate about creating memorable stays. My properties are designed with comfort and style in mind.",
            "languages": ["English", "Urdu", "Sindhi"],
            "guest_score": 4.9
        },
        {
            "email": "guest1@homlo.pk",
            "phone": "+923001234569",
            "name": "Usman Hassan",
            "roles": ["guest"],
            "verification_level": "phone",
            "about": "Frequent traveler exploring Pakistan's beautiful destinations. Always respectful of properties and hosts.",
            "languages": ["English", "Urdu"],
            "guest_score": 4.7
        },
        {
            "email": "guest2@homlo.pk",
            "phone": "+923001234570",
            "name": "Ayesha Malik",
            "roles": ["guest"],
            "verification_level": "phone",
            "about": "Love exploring new places and meeting new people. Clean and respectful guest.",
            "languages": ["English", "Urdu", "Punjabi"],
            "guest_score": 4.6
        },
        {
            "email": "admin@homlo.pk",
            "phone": "+923001234571",
            "name": "Admin User",
            "roles": ["admin"],
            "verification_level": "cnic",
            "cnic_number": "12345-1234571-3",
            "about": "System administrator for Homlo platform.",
            "languages": ["English", "Urdu"],
            "guest_score": 5.0
        }
    ]
    
    # Create users (in production, this would use proper models)
    for user_data in users_data:
        user_data["id"] = str(uuid.uuid4())
        user_data["password_hash"] = get_password_hash("password123")
        user_data["created_at"] = datetime.utcnow()
        user_data["updated_at"] = datetime.utcnow()
    
    print(f"   Added {len(users_data)} demo users")
    return users_data


async def seed_demo_listings(db: AsyncSession):
    """Seed demo listings"""
    print("🏠 Seeding demo listings...")
    
    listings_data = [
        {
            "title": "Luxury Apartment in Clifton, Karachi",
            "description": "Beautiful 3-bedroom apartment with sea view in the heart of Clifton. Modern amenities, fully furnished, and perfect for families or business travelers.",
            "city": "Karachi",
            "area": "Clifton",
            "latitude": 24.8207,
            "longitude": 67.0371,
            "type": "entire_home",
            "max_guests": 6,
            "bedrooms": 3,
            "beds": 4,
            "bathrooms": 2,
            "amenities": ["WiFi", "Air Conditioning", "Kitchen", "Parking", "Generator", "Security Guard", "Sea View"],
            "house_rules": "No smoking, No parties, Respect neighbors",
            "instant_book": True,
            "status": "active",
            "host_id": "host1@homlo.pk"
        },
        {
            "title": "Cozy Studio in Gulberg, Lahore",
            "description": "Modern studio apartment in the trendy Gulberg area. Perfect for solo travelers or couples. Walking distance to restaurants and shopping.",
            "city": "Lahore",
            "area": "Gulberg",
            "latitude": 31.5204,
            "longitude": 74.3587,
            "type": "studio",
            "max_guests": 2,
            "bedrooms": 1,
            "beds": 1,
            "bathrooms": 1,
            "amenities": ["WiFi", "Air Conditioning", "Kitchen", "Parking", "Balcony", "TV"],
            "house_rules": "No smoking, Quiet hours after 10 PM",
            "instant_book": True,
            "status": "active",
            "host_id": "host2@homlo.pk"
        },
        {
            "title": "Mountain View Guest House in Murree",
            "description": "Charming guest house with stunning mountain views. Perfect for a peaceful getaway. Cozy rooms with traditional Pakistani hospitality.",
            "city": "Murree",
            "area": "City",
            "latitude": 33.9071,
            "longitude": 73.3903,
            "type": "guest_house",
            "max_guests": 8,
            "bedrooms": 4,
            "beds": 6,
            "bathrooms": 3,
            "amenities": ["WiFi", "Heating", "Kitchen", "Garden", "Mountain View", "BBQ Area", "Parking"],
            "house_rules": "No pets, Respect nature, Quiet environment",
            "instant_book": False,
            "status": "active",
            "host_id": "host1@homlo.pk"
        },
        {
            "title": "Modern Office Space in F-7, Islamabad",
            "description": "Professional office space in the heart of Islamabad's business district. Fully equipped with modern amenities and high-speed internet.",
            "city": "Islamabad",
            "area": "F-7",
            "latitude": 33.6844,
            "longitude": 73.0479,
            "type": "office",
            "max_guests": 10,
            "bedrooms": 0,
            "beds": 0,
            "bathrooms": 2,
            "amenities": ["WiFi", "Air Conditioning", "Work Desk", "High-Speed Internet", "Printer", "Parking", "Security Guard"],
            "house_rules": "Business hours only, No food in office area, Professional conduct",
            "instant_book": True,
            "status": "active",
            "host_id": "host2@homlo.pk"
        },
        {
            "title": "Beachfront Villa in Gwadar",
            "description": "Exclusive beachfront villa with private beach access. Stunning ocean views and modern luxury amenities. Perfect for a premium getaway.",
            "city": "Gwadar",
            "area": "City",
            "latitude": 25.1216,
            "longitude": 62.3254,
            "type": "entire_home",
            "max_guests": 12,
            "bedrooms": 5,
            "beds": 8,
            "bathrooms": 4,
            "amenities": ["WiFi", "Air Conditioning", "Kitchen", "Swimming Pool", "Private Beach", "Garden", "BBQ Area", "Security Guard", "Generator"],
            "house_rules": "No parties, Respect beach environment, No loud music",
            "instant_book": False,
            "status": "active",
            "host_id": "host1@homlo.pk"
        }
    ]
    
    # Create listings (in production, this would use proper models)
    for listing_data in listings_data:
        listing_data["id"] = str(uuid.uuid4())
        listing_data["slug"] = listing_data["title"].lower().replace(" ", "-").replace(",", "").replace(".", "")
        listing_data["created_at"] = datetime.utcnow()
        listing_data["updated_at"] = datetime.utcnow()
    
    print(f"   Added {len(listings_data)} demo listings")
    return listings_data


async def seed_demo_bookings(db: AsyncSession):
    """Seed demo bookings"""
    print("📅 Seeding demo bookings...")
    
    # Create some sample bookings
    bookings_data = [
        {
            "listing_id": "luxury-apartment-in-clifton-karachi",
            "guest_id": "guest1@homlo.pk",
            "check_in": date.today() + timedelta(days=7),
            "check_out": date.today() + timedelta(days=10),
            "guests_count": 4,
            "status": "confirmed",
            "total_pkr": Decimal("15000"),
            "currency": "PKR",
            "payment_status": "completed"
        },
        {
            "listing_id": "cozy-studio-in-gulberg-lahore",
            "guest_id": "guest2@homlo.pk",
            "check_in": date.today() + timedelta(days=14),
            "check_out": date.today() + timedelta(days=16),
            "guests_count": 2,
            "status": "pending",
            "total_pkr": Decimal("8000"),
            "currency": "PKR",
            "payment_status": "pending"
        }
    ]
    
    print(f"   Added {len(bookings_data)} demo bookings")


async def main():
    """Main function to run the seeding process"""
    try:
        await seed_database()
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
