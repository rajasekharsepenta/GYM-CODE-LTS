from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uvicorn
from datetime import datetime, timedelta
import random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Elite Fitness API",
    description="Premium fitness management system API for Elite Fitness gym",
    version="3.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enhanced CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
# Data Models
# ===============================

class GymClass(BaseModel):
    id: int
    name: str
    instructor: str
    time: str
    duration: str
    difficulty: str
    capacity: int
    price: float
    available_spots: int
    description: str
    benefits: List[str]
    image_url: Optional[str] = None
    location: Optional[str] = "Main Studio"
    equipment_needed: Optional[List[str]] = []

class Trainer(BaseModel):
    id: int
    name: str
    specialty: str
    experience: str
    rating: float
    image: str
    hourly_rate: float
    available_slots: List[str]
    bio: str
    certifications: List[str]
    languages: Optional[List[str]] = ["English"]
    social_media: Optional[Dict[str, str]] = {}

class Equipment(BaseModel):
    id: int
    name: str
    category: str
    status: str
    capacity: int
    available_slots: int
    location: str
    description: str
    instructions: str
    brand: Optional[str] = "Premium"
    model: Optional[str] = "Pro"
    maintenance_date: Optional[str] = None

class Membership(BaseModel):
    id: int
    name: str
    price: int
    features: List[str]
    popular: bool
    duration: str
    description: str
    color_scheme: Optional[str] = "orange"
    max_guests: Optional[int] = 0
    personal_training_sessions: Optional[int] = 0

class BookingRequest(BaseModel):
    user_id: Optional[int] = 1
    user_name: Optional[str] = "John Doe"
    user_email: Optional[str] = "john@example.com"
    user_phone: Optional[str] = "+1 (555) 123-4567"
    preferred_time: Optional[str] = None
    notes: Optional[str] = None

class SearchRequest(BaseModel):
    query: str
    category: Optional[str] = ""

class ContactRequest(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    message: str
    subject: Optional[str] = "General Inquiry"

# ===============================
# Sample Data
# ===============================

CLASSES = [
    GymClass(
        id=1, name="HIIT Inferno", instructor="Sarah Johnson", 
        time="6:00 AM", duration="45 min", difficulty="Advanced", capacity=20, 
        price=35.0, available_spots=15,
        description="High-intensity interval training that will push your limits and transform your body",
        benefits=["Burns 400+ calories", "Improves cardiovascular health", "Builds endurance", "Boosts metabolism"],
        location="Studio A",
        equipment_needed=["Battle ropes", "Kettlebells", "Medicine balls"]
    ),
    GymClass(
        id=2, name="Zen Flow Yoga", instructor="Mike Chen", 
        time="8:00 AM", duration="60 min", difficulty="Beginner", capacity=15,
        price=25.0, available_spots=12,
        description="Peaceful yoga flow for mind and body harmony, perfect for stress relief",
        benefits=["Improves flexibility", "Reduces stress", "Better sleep", "Mindfulness"],
        location="Yoga Studio",
        equipment_needed=["Yoga mats", "Blocks", "Straps"]
    ),
    GymClass(
        id=3, name="Iron Strength", instructor="Emma Davis", 
        time="10:00 AM", duration="50 min", difficulty="Intermediate", capacity=12,
        price=40.0, available_spots=8,
        description="Comprehensive strength training with free weights and machines",
        benefits=["Builds muscle mass", "Increases bone density", "Boosts metabolism", "Improves posture"],
        location="Weight Room",
        equipment_needed=["Barbells", "Dumbbells", "Bench press"]
    ),
    GymClass(
        id=4, name="Core Destroyer", instructor="Lisa Wong", 
        time="12:00 PM", duration="30 min", difficulty="Intermediate", capacity=18,
        price=20.0, available_spots=16,
        description="Intense core workout targeting all abdominal muscles for a strong foundation",
        benefits=["Stronger core", "Better posture", "Injury prevention", "Improved balance"],
        location="Studio B",
        equipment_needed=["Exercise mats", "Resistance bands"]
    ),
    GymClass(
        id=5, name="CrossFit Elite", instructor="David Miller", 
        time="2:00 PM", duration="60 min", difficulty="Advanced", capacity=15,
        price=45.0, available_spots=10,
        description="Elite CrossFit training for serious athletes seeking peak performance",
        benefits=["Functional fitness", "Athletic performance", "Mental toughness", "Full-body conditioning"],
        location="CrossFit Box",
        equipment_needed=["Olympic bars", "Plates", "Pull-up bars", "Boxes"]
    ),
    GymClass(
        id=6, name="Dance Cardio", instructor="Maria Garcia", 
        time="4:00 PM", duration="45 min", difficulty="Beginner", capacity=25,
        price=22.0, available_spots=20,
        description="Fun dance-based cardio workout that doesn't feel like exercise",
        benefits=["Cardio fitness", "Coordination", "Stress relief", "Social interaction"],
        location="Dance Studio",
        equipment_needed=[]
    ),
    GymClass(
        id=7, name="Boxing Fundamentals", instructor="Tony Rodriguez", 
        time="6:00 PM", duration="60 min", difficulty="Intermediate", capacity=16,
        price=38.0, available_spots=14,
        description="Learn boxing basics while getting an intense full-body workout",
        benefits=["Self-defense skills", "Upper body strength", "Stress relief", "Cardio fitness"],
        location="Boxing Ring",
        equipment_needed=["Boxing gloves", "Heavy bags", "Speed bags"]
    ),
    GymClass(
        id=8, name="Spin Revolution", instructor="Jessica Kim", 
        time="7:00 AM", duration="45 min", difficulty="Intermediate", capacity=20,
        price=30.0, available_spots=18,
        description="High-energy spinning class with motivating music and challenging intervals",
        benefits=["Leg strength", "Cardiovascular endurance", "Mental focus", "Low impact"],
        location="Spin Studio",
        equipment_needed=["Spin bikes"]
    )
]

TRAINERS = [
    Trainer(
        id=1, name="Sarah Johnson", specialty="HIIT & Cardio", 
        experience="5 years", rating=4.9, hourly_rate=85.0,
        image="https://images.unsplash.com/photo-1594736797933-d0300ba73cd1?w=300&h=300&fit=crop&crop=face",
        available_slots=["9:00 AM", "11:00 AM", "2:00 PM", "4:00 PM"],
        bio="Certified personal trainer specializing in high-intensity workouts and cardiovascular conditioning. Former competitive athlete with a passion for helping clients achieve their fitness goals.",
        certifications=["NASM-CPT", "HIIT Specialist", "Nutrition Coach"],
        languages=["English", "Spanish"],
        social_media={"instagram": "@sarahfitness", "twitter": "@sarahjohnsonfit"}
    ),
    Trainer(
        id=2, name="Mike Chen", specialty="Yoga & Flexibility", 
        experience="8 years", rating=4.8, hourly_rate=75.0,
        image="https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=300&h=300&fit=crop&crop=face",
        available_slots=["8:00 AM", "10:00 AM", "1:00 PM", "3:00 PM"],
        bio="Experienced yoga instructor focused on flexibility, mindfulness, and injury prevention. Trained in multiple yoga styles including Hatha, Vinyasa, and Yin.",
        certifications=["RYT-500", "Yin Yoga Specialist", "Meditation Teacher"],
        languages=["English", "Mandarin"],
        social_media={"instagram": "@mikeyoga", "website": "mikechenyang.com"}
    ),
    Trainer(
        id=3, name="Emma Davis", specialty="Strength Training", 
        experience="6 years", rating=4.9, hourly_rate=90.0,
        image="https://images.unsplash.com/photo-1559850350-2d3d38a7e1a2?w=300&h=300&fit=crop&crop=face",
        available_slots=["7:00 AM", "9:00 AM", "12:00 PM", "5:00 PM"],
        bio="Strength and conditioning specialist helping clients build muscle and increase power. Former powerlifting competitor with expertise in Olympic lifting.",
        certifications=["CSCS", "Olympic Lifting Coach", "Powerlifting Specialist"],
        languages=["English"],
        social_media={"instagram": "@emmastrength", "youtube": "EmmaFitnessTV"}
    ),
    Trainer(
        id=4, name="David Miller", specialty="CrossFit", 
        experience="7 years", rating=4.7, hourly_rate=95.0,
        image="https://images.unsplash.com/photo-1567013127542-490d757e51cd?w=300&h=300&fit=crop&crop=face",
        available_slots=["6:00 AM", "10:00 AM", "1:00 PM", "6:00 PM"],
        bio="CrossFit Level 3 trainer specializing in functional fitness and athletic performance. Former military with expertise in tactical fitness.",
        certifications=["CF-L3", "Gymnastics Coach", "Olympic Weightlifting"],
        languages=["English"],
        social_media={"instagram": "@davidcrossfit"}
    ),
    Trainer(
        id=5, name="Lisa Wong", specialty="Pilates & Core", 
        experience="4 years", rating=4.8, hourly_rate=80.0,
        image="https://images.unsplash.com/photo-1609505848912-b7c3b8b4beda?w=300&h=300&fit=crop&crop=face",
        available_slots=["8:00 AM", "11:00 AM", "2:00 PM", "4:00 PM"],
        bio="Pilates instructor focused on core strength, posture, and functional movement. Specializes in rehabilitation and injury prevention.",
        certifications=["PMA-CPT", "Mat Pilates", "Reformer Certified"],
        languages=["English", "Cantonese"],
        social_media={"instagram": "@lisapilates"}
    ),
    Trainer(
        id=6, name="Tony Rodriguez", specialty="Boxing & Combat", 
        experience="9 years", rating=4.9, hourly_rate=100.0,
        image="https://images.unsplash.com/photo-1605296867304-46d5465a13f1?w=300&h=300&fit=crop&crop=face",
        available_slots=["7:00 AM", "12:00 PM", "3:00 PM", "7:00 PM"],
        bio="Professional boxing coach and former competitive fighter. Specializes in technique, conditioning, and mental toughness.",
        certifications=["USA Boxing Certified", "Kickboxing Instructor", "Self-Defense Specialist"],
        languages=["English", "Spanish"],
        social_media={"instagram": "@tonyboxing", "facebook": "TonyRodriguezBoxing"}
    )
]

EQUIPMENT = [
    Equipment(
        id=1, name="Treadmill", category="cardio", status="Available", 
        capacity=1, available_slots=15, location="Cardio Zone A",
        description="High-performance treadmill with advanced cushioning system and interactive display",
        instructions="Start with 5-minute warm-up, gradually increase speed. Maximum speed: 12 mph",
        brand="TechnoGym", model="Run Personal", maintenance_date="2024-01-15"
    ),
    Equipment(
        id=2, name="Elliptical", category="cardio", status="Available", 
        capacity=1, available_slots=12, location="Cardio Zone A",
        description="Low-impact elliptical trainer for full-body cardiovascular workout",
        instructions="Maintain upright posture, use arm handles for upper body engagement",
        brand="Precor", model="EFX 885", maintenance_date="2024-01-20"
    ),
    Equipment(
        id=3, name="Stationary Bike", category="cardio", status="Available", 
        capacity=1, available_slots=18, location="Cardio Zone B",
        description="Professional spin bike with magnetic resistance and performance tracking",
        instructions="Adjust seat height to hip level, start with light resistance",
        brand="Peloton", model="Bike+", maintenance_date="2024-01-10"
    ),
    Equipment(
        id=4, name="Rowing Machine", category="cardio", status="Available", 
        capacity=1, available_slots=10, location="Cardio Zone B",
        description="Water resistance rowing machine for full-body cardio and strength",
        instructions="Drive with legs first, then lean back and pull with arms",
        brand="Concept2", model="Model D", maintenance_date="2024-01-25"
    ),
    Equipment(
        id=5, name="Dumbbells", category="strength", status="Available", 
        capacity=4, available_slots=20, location="Free Weights Zone",
        description="Complete set of dumbbells from 5-100 lbs with rubber coating",
        instructions="Start with lighter weights, focus on proper form over heavy weight",
        brand="Rogue Fitness", model="Rubber Hex", maintenance_date="2024-02-01"
    ),
    Equipment(
        id=6, name="Barbell", category="strength", status="Available", 
        capacity=2, available_slots=8, location="Free Weights Zone",
        description="Olympic barbells with safety squat racks and Olympic plates",
        instructions="Always use safety bars, warm up with empty bar first",
        brand="Eleiko", model="Sport Training Bar", maintenance_date="2024-01-18"
    ),
    Equipment(
        id=7, name="Cable Machine", category="strength", status="Available", 
        capacity=2, available_slots=14, location="Strength Training Zone",
        description="Multi-station cable machine with various attachments for versatile training",
        instructions="Adjust pulley height for different exercises, maintain controlled movements",
        brand="Life Fitness", model="Dual Adjustable Pulley", maintenance_date="2024-01-22"
    ),
    Equipment(
        id=8, name="Bench Press", category="strength", status="Available", 
        capacity=1, available_slots=6, location="Strength Training Zone",
        description="Olympic bench press with safety spotters and adjustable rack",
        instructions="Always use spotter for heavy weights, control the descent",
        brand="Rogue Fitness", model="Monster Bench", maintenance_date="2024-01-12"
    ),
    Equipment(
        id=9, name="Kettlebells", category="functional", status="Available", 
        capacity=6, available_slots=25, location="Functional Training Area",
        description="Russian kettlebells ranging from 8kg to 48kg for functional strength",
        instructions="Start with hip hinge movement, progress gradually in weight",
        brand="Kettlebell Kings", model="Powder Coat", maintenance_date="2024-01-30"
    ),
    Equipment(
        id=10, name="Resistance Bands", category="functional", status="Available", 
        capacity=10, available_slots=30, location="Functional Training Area",
        description="Various resistance levels for rehabilitation and strength training",
        instructions="Check bands for wear before use, anchor securely",
        brand="Bodylastics", model="Max Tension Set", maintenance_date="2024-02-05"
    ),
    Equipment(
        id=11, name="Medicine Ball", category="functional", status="Available", 
        capacity=8, available_slots=22, location="Functional Training Area",
        description="Weighted medicine balls from 6-30 lbs for explosive power training",
        instructions="Use for slam exercises and rotational movements",
        brand="Dynamax", model="Standard", maintenance_date="2024-01-28"
    ),
    Equipment(
        id=12, name="Battle Ropes", category="functional", status="Available", 
        capacity=2, available_slots=12, location="Functional Training Area",
        description="Heavy battle ropes for high-intensity interval training",
        instructions="Maintain athletic stance, alternate arm waves for 30-60 seconds",
        brand="Rep Fitness", model="Battle Rope 2\"", maintenance_date="2024-01-14"
    ),
    Equipment(
        id=13, name="Smith Machine", category="strength", status="Maintenance", 
        capacity=1, available_slots=0, location="Strength Training Zone",
        description="Guided barbell system for safe solo training with built-in safety stops",
        instructions="Set safety stops at appropriate height, maintain proper form",
        brand="Hammer Strength", model="Linear Smith Machine", maintenance_date="2024-01-08"
    ),
    Equipment(
        id=14, name="Leg Press", category="strength", status="Available", 
        capacity=1, available_slots=8, location="Strength Training Zone",
        description="45-degree leg press machine for lower body strength development",
        instructions="Keep knees aligned with toes, control the descent",
        brand="TechnoGym", model="Selection 900", maintenance_date="2024-01-16"
    ),
    Equipment(
        id=15, name="Pull-up Bar", category="functional", status="Available", 
        capacity=3, available_slots=15, location="Functional Training Area",
        description="Multi-grip pull-up station with assistance bands available",
        instructions="Use full range of motion, engage core throughout movement",
        brand="Rogue Fitness", model="Stall Bar", maintenance_date="2024-01-26"
    )
]

MEMBERSHIPS = [
    Membership(
        id=1, name="Essential", price=39, duration="Monthly",
        features=[
            "Gym Access (6 AM - 10 PM)",
            "Locker Room & Showers", 
            "Basic Equipment Access",
            "Mobile App Access",
            "Free Fitness Assessment",
            "Guest Pass (1/month)"
        ],
        popular=False,
        description="Perfect for fitness beginners and casual gym-goers who want access to quality equipment",
        color_scheme="gray",
        max_guests=1,
        personal_training_sessions=0
    ),
    Membership(
        id=2, name="Premium", price=69, duration="Monthly",
        features=[
            "24/7 Gym Access",
            "All Group Classes Included",
            "2 Personal Training Sessions/month",
            "Nutrition Consultation",
            "Guest Passes (3/month)",
            "Priority Equipment Booking",
            "Towel Service",
            "Sauna & Steam Room Access"
        ],
        popular=True,
        description="Complete fitness package for serious fitness enthusiasts who want it all",
        color_scheme="orange",
        max_guests=3,
        personal_training_sessions=2
    ),
    Membership(
        id=3, name="Elite", price=99, duration="Monthly",
        features=[
            "24/7 Premium Access",
            "Unlimited Personal Training",
            "Unlimited Group Classes",
            "Recovery & Spa Zone Access",
            "Unlimited Guest Passes",
            "Meal Planning Service",
            "Priority Support Hotline",
            "Exclusive Member Events",
            "Massage Therapy (2/month)",
            "Supplement Discounts"
        ],
        popular=False,
        description="Ultimate luxury fitness experience with all premium amenities and services",
        color_scheme="gold",
        max_guests=999,
        personal_training_sessions=999
    ),
    Membership(
        id=4, name="Student", price=29, duration="Monthly",
        features=[
            "Gym Access (6 AM - 6 PM)",
            "Basic Equipment Access",
            "Select Group Classes (3/week)",
            "Study Area with WiFi",
            "Student ID Required",
            "Locker Room Access"
        ],
        popular=False,
        description="Affordable option for students with valid student ID",
        color_scheme="blue",
        max_guests=0,
        personal_training_sessions=0
    )
]

# Enhanced Statistics
STATS = {
    "total_members": 2847,
    "total_classes": 156,
    "total_trainers": 28,
    "total_equipment": 285,
    "monthly_check_ins": 15600,
    "satisfaction_rate": 4.9,
    "average_workout_time": 78,
    "calories_burned_monthly": 3200000,
    "member_retention_rate": 94.5,
    "peak_hours": ["6-8 AM", "5-7 PM"],
    "busiest_day": "Monday",
    "most_popular_class": "HIIT Inferno"
}

# ===============================
# API Endpoints
# ===============================

@app.get("/", tags=["Root"])
async def root():
    """Welcome endpoint with API information"""
    return {
        "message": "🏋️‍♂️ Elite Fitness API v3.1 - Premium Gym Management System",
        "version": "3.1.0",
        "status": "active",
        "timestamp": datetime.now().isoformat(),
        "features": [
            "Class Management", "Trainer Booking", "Equipment Tracking", 
            "Membership Plans", "Real-time Stats", "Advanced Search"
        ],
        "endpoints": {
            "documentation": "/docs",
            "stats": "/api/stats",
            "classes": "/api/classes",
            "trainers": "/api/trainers",
            "equipment": "/api/equipment",
            "memberships": "/api/memberships"
        }
    }

@app.get("/api/stats", tags=["Statistics"])
async def get_stats():
    """Get comprehensive gym statistics and metrics"""
    logger.info("Stats requested")
    
    # Add some dynamic elements
    current_stats = STATS.copy()
    current_stats["last_updated"] = datetime.now().isoformat()
    current_stats["active_classes_today"] = len([c for c in CLASSES if c.available_spots > 0])
    current_stats["available_trainers"] = len([t for t in TRAINERS if len(t.available_slots) > 0])
    current_stats["equipment_in_use"] = len([e for e in EQUIPMENT if e.status == "In Use"])
    
    return current_stats

@app.get("/api/classes", tags=["Classes"])
async def get_classes(
    difficulty: Optional[str] = Query(None, description="Filter by difficulty: beginner, intermediate, advanced"),
    instructor: Optional[str] = Query(None, description="Filter by instructor name"),
    time_of_day: Optional[str] = Query(None, description="Filter by time: morning, afternoon, evening"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page")
):
    """Get fitness classes with optional filtering and pagination"""
    logger.info(f"Classes requested - difficulty: {difficulty}, instructor: {instructor}, page: {page}")
    
    filtered_classes = CLASSES.copy()
    
    # Apply filters
    if difficulty and difficulty.lower() != "all":
        filtered_classes = [c for c in filtered_classes if c.difficulty.lower() == difficulty.lower()]
    
    if instructor:
        filtered_classes = [c for c in filtered_classes if instructor.lower() in c.instructor.lower()]
    
    if time_of_day:
        time_filters = {
            "morning": lambda t: int(t.split(':')[0]) < 12,
            "afternoon": lambda t: 12 <= int(t.split(':')[0]) < 17,
            "evening": lambda t: int(t.split(':')[0]) >= 17
        }
        if time_of_day.lower() in time_filters:
            filtered_classes = [c for c in filtered_classes if time_filters[time_of_day.lower()](c.time)]
    
    # Pagination
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_classes = filtered_classes[start_idx:end_idx]
    
    return {
        "classes": paginated_classes,
        "total": len(filtered_classes),
        "page": page,
        "limit": limit,
        "has_more": end_idx < len(filtered_classes),
        "total_pages": (len(filtered_classes) + limit - 1) // limit,
        "filters_applied": {
            "difficulty": difficulty,
            "instructor": instructor,
            "time_of_day": time_of_day
        }
    }

@app.get("/api/classes/{class_id}", tags=["Classes"])
async def get_class_detail(class_id: int):
    """Get detailed information about a specific class"""
    class_item = next((c for c in CLASSES if c.id == class_id), None)
    if not class_item:
        raise HTTPException(status_code=404, detail="Class not found")
    
    logger.info(f"Class detail requested for ID: {class_id}")
    return class_item

@app.get("/api/trainers", tags=["Trainers"])
async def get_trainers(
    specialty: Optional[str] = Query(None, description="Filter by specialty"),
    available_only: bool = Query(False, description="Show only trainers with available slots"),
    min_rating: float = Query(0.0, ge=0.0, le=5.0, description="Minimum rating"),
    all: bool = Query(False, description="Return all trainers without limit")
):
    """Get personal trainers with optional filtering"""
    logger.info(f"Trainers requested - specialty: {specialty}, available_only: {available_only}")
    
    filtered_trainers = TRAINERS.copy()
    
    # Apply filters
    if specialty:
        filtered_trainers = [t for t in filtered_trainers if specialty.lower() in t.specialty.lower()]
    
    if available_only:
        filtered_trainers = [t for t in filtered_trainers if len(t.available_slots) > 0]
    
    if min_rating > 0:
        filtered_trainers = [t for t in filtered_trainers if t.rating >= min_rating]
    
    # Limit results unless 'all' is requested
    if not all:
        filtered_trainers = filtered_trainers[:6]
    
    return {
        "trainers": filtered_trainers,
        "total": len(TRAINERS),
        "filtered_count": len(filtered_trainers),
        "specialties": list(set([t.specialty for t in TRAINERS])),
        "average_rating": sum([t.rating for t in TRAINERS]) / len(TRAINERS),
        "price_range": {
            "min": min([t.hourly_rate for t in TRAINERS]),
            "max": max([t.hourly_rate for t in TRAINERS])
        }
    }

@app.get("/api/trainers/{trainer_id}", tags=["Trainers"])
async def get_trainer_detail(trainer_id: int):
    """Get detailed information about a specific trainer"""
    trainer = next((t for t in TRAINERS if t.id == trainer_id), None)
    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")
    
    logger.info(f"Trainer detail requested for ID: {trainer_id}")
    return trainer

@app.get("/api/equipment", tags=["Equipment"])
async def get_equipment(
    category: Optional[str] = Query(None, description="Filter by category: cardio, strength, functional"),
    status: Optional[str] = Query(None, description="Filter by status: Available, In Use, Maintenance"),
    location: Optional[str] = Query(None, description="Filter by location"),
    available_only: bool = Query(False, description="Show only available equipment")
):
    """Get gym equipment with optional filtering"""
    logger.info(f"Equipment requested - category: {category}, status: {status}")
    
    filtered_equipment = EQUIPMENT.copy()
    
    # Apply filters
    if category and category.lower() != "all":
        filtered_equipment = [e for e in filtered_equipment if e.category.lower() == category.lower()]
    
    if status:
        filtered_equipment = [e for e in filtered_equipment if e.status.lower() == status.lower()]
    
    if location:
        filtered_equipment = [e for e in filtered_equipment if location.lower() in e.location.lower()]
    
    if available_only:
        filtered_equipment = [e for e in filtered_equipment if e.status == "Available" and e.available_slots > 0]
    
    return {
        "equipment": filtered_equipment,
        "total": len(filtered_equipment),
        "categories": list(set([e.category for e in EQUIPMENT])),
        "locations": list(set([e.location for e in EQUIPMENT])),
        "status_summary": {
            "available": len([e for e in EQUIPMENT if e.status == "Available"]),
            "in_use": len([e for e in EQUIPMENT if e.status == "In Use"]),
            "maintenance": len([e for e in EQUIPMENT if e.status == "Maintenance"])
        }
    }

@app.get("/api/equipment/{equipment_id}", tags=["Equipment"])
async def get_equipment_detail(equipment_id: int):
    """Get detailed information about specific equipment"""
    equipment = next((e for e in EQUIPMENT if e.id == equipment_id), None)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    logger.info(f"Equipment detail requested for ID: {equipment_id}")
    return equipment

@app.get("/api/memberships", tags=["Memberships"])
async def get_memberships():
    """Get membership plans"""
    logger.info("Memberships requested")
    
    return {
        "memberships": MEMBERSHIPS,
        "total": len(MEMBERSHIPS),
        "most_popular": next((m for m in MEMBERSHIPS if m.popular), None),
        "price_range": {
            "min": min([m.price for m in MEMBERSHIPS]),
            "max": max([m.price for m in MEMBERSHIPS])
        },
        "features_comparison": {
            m.name: len(m.features) for m in MEMBERSHIPS
        }
    }

@app.get("/api/memberships/{membership_id}", tags=["Memberships"])
async def get_membership_detail(membership_id: int):
    """Get detailed information about a specific membership plan"""
    membership = next((m for m in MEMBERSHIPS if m.id == membership_id), None)
    if not membership:
        raise HTTPException(status_code=404, detail="Membership plan not found")
    
    logger.info(f"Membership detail requested for ID: {membership_id}")
    return membership

@app.post("/api/search", tags=["Search"])
async def search(request: SearchRequest):
    """Advanced search across all gym resources"""
    logger.info(f"Search requested - query: {request.query}, category: {request.category}")
    
    results = []
    query_lower = request.query.lower()
    
    # Search classes
    if not request.category or request.category == "classes":
        for class_item in CLASSES:
            if (query_lower in class_item.name.lower() or 
                query_lower in class_item.instructor.lower() or
                query_lower in class_item.difficulty.lower() or
                query_lower in class_item.description.lower() or
                any(query_lower in benefit.lower() for benefit in class_item.benefits)):
                
                match_score = 1.0
                if query_lower in class_item.name.lower():
                    match_score = 1.0
                elif query_lower in class_item.instructor.lower():
                    match_score = 0.9
                elif query_lower in class_item.difficulty.lower():
                    match_score = 0.8
                else:
                    match_score = 0.7
                
                results.append({**class_item.dict(), "type": "class", "match_score": match_score})
    
    # Search trainers
    if not request.category or request.category == "trainers":
        for trainer in TRAINERS:
            if (query_lower in trainer.name.lower() or 
                query_lower in trainer.specialty.lower() or
                query_lower in trainer.bio.lower() or
                any(query_lower in cert.lower() for cert in trainer.certifications)):
                
                match_score = 1.0
                if query_lower in trainer.name.lower():
                    match_score = 1.0
                elif query_lower in trainer.specialty.lower():
                    match_score = 0.9
                else:
                    match_score = 0.8
                
                results.append({**trainer.dict(), "type": "trainer", "match_score": match_score})
    
    # Search equipment
    if not request.category or request.category == "equipment":
        for equipment in EQUIPMENT:
            if (query_lower in equipment.name.lower() or 
                query_lower in equipment.category.lower() or
                query_lower in equipment.description.lower() or
                query_lower in equipment.brand.lower() if equipment.brand else False):
                
                match_score = 1.0
                if query_lower in equipment.name.lower():
                    match_score = 1.0
                elif query_lower in equipment.category.lower():
                    match_score = 0.9
                else:
                    match_score = 0.7
                
                results.append({**equipment.dict(), "type": "equipment", "match_score": match_score})
    
    # Sort by relevance
    results.sort(key=lambda x: x.get("match_score", 0), reverse=True)
    
    return {
        "results": results[:20],  # Limit results
        "total_found": len(results),
        "query": request.query,
        "category": request.category,
        "search_time": f"{random.uniform(0.05, 0.2):.3f}s",
        "suggestions": _get_search_suggestions(request.query) if len(results) == 0 else []
    }

def _get_search_suggestions(query: str) -> List[str]:
    """Generate search suggestions for empty results"""
    suggestions = []
    common_terms = ["yoga", "strength", "cardio", "hiit", "boxing", "pilates", "crossfit"]
    
    for term in common_terms:
        if term not in query.lower():
            suggestions.append(term)
    
    return suggestions[:3]

# ===============================
# Booking Endpoints
# ===============================

@app.post("/api/book-class/{class_id}", tags=["Bookings"])
async def book_class(class_id: int, booking: Optional[BookingRequest] = None):
    """Book a fitness class"""
    logger.info(f"Class booking requested for ID: {class_id}")
    
    class_item = next((c for c in CLASSES if c.id == class_id), None)
    if not class_item:
        raise HTTPException(status_code=404, detail="Class not found")
    
    if class_item.available_spots <= 0:
        raise HTTPException(status_code=400, detail="Class is fully booked")
    
    # Simulate booking
    class_item.available_spots -= 1
    booking_id = f"CLS-{class_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    session_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    booking_details = {
        "message": f"Successfully booked {class_item.name}!",
        "booking_id": booking_id,
        "class_name": class_item.name,
        "instructor": class_item.instructor,
        "scheduled_time": class_item.time,
        "duration": class_item.duration,
        "session_date": session_date,
        "location": class_item.location,
        "price": f"${class_item.price}",
        "spots_remaining": class_item.available_spots,
        "booking_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "confirmation_code": f"CF{random.randint(1000, 9999)}",
        "customer_info": {
            "name": booking.user_name if booking else "John Doe",
            "email": booking.user_email if booking else "john@example.com"
        }
    }
    
    logger.info(f"Class booked successfully: {booking_id}")
    return booking_details

@app.post("/api/book-trainer/{trainer_id}", tags=["Bookings"])
async def book_trainer(trainer_id: int, booking: Optional[BookingRequest] = None):
    """Book a personal training session"""
    logger.info(f"Trainer booking requested for ID: {trainer_id}")
    
    trainer = next((t for t in TRAINERS if t.id == trainer_id), None)
    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")
    
    if not trainer.available_slots:
        raise HTTPException(status_code=400, detail="Trainer has no available slots")
    
    # Simulate booking
    booked_slot = trainer.available_slots.pop(0) if trainer.available_slots else "TBD"
    booking_id = f"TRN-{trainer_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    session_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    
    booking_details = {
        "message": f"Training session booked with {trainer.name}!",
        "booking_id": booking_id,
        "trainer_name": trainer.name,
        "specialty": trainer.specialty,
        "scheduled_time": booked_slot,
        "session_date": session_date,
        "duration": "60 minutes",
        "hourly_rate": f"${trainer.hourly_rate}",
        "total_cost": f"${trainer.hourly_rate}",
        "booking_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "confirmation_code": f"PT{random.randint(1000, 9999)}",
        "trainer_contact": "Contact info will be provided 24h before session",
        "customer_info": {
            "name": booking.user_name if booking else "John Doe",
            "email": booking.user_email if booking else "john@example.com"
        }
    }
    
    logger.info(f"Trainer session booked successfully: {booking_id}")
    return booking_details

@app.post("/api/reserve-equipment/{equipment_id}", tags=["Bookings"])
async def reserve_equipment(equipment_id: int, booking: Optional[BookingRequest] = None):
    """Reserve gym equipment"""
    logger.info(f"Equipment reservation requested for ID: {equipment_id}")
    
    equipment = next((e for e in EQUIPMENT if e.id == equipment_id), None)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    if equipment.available_slots <= 0:
        raise HTTPException(status_code=400, detail="Equipment is fully reserved")
    
    if equipment.status != "Available":
        raise HTTPException(status_code=400, detail=f"Equipment is currently {equipment.status.lower()}")
    
    # Simulate reservation
    equipment.available_slots -= 1
    reservation_id = f"EQP-{equipment_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    reservation_details = {
        "message": f"Equipment reserved: {equipment.name}",
        "reservation_id": reservation_id,
        "equipment_name": equipment.name,
        "category": equipment.category,
        "location": equipment.location,
        "brand_model": f"{equipment.brand} {equipment.model}",
        "reserved_time_slot": "Next available: 30 minutes",
        "duration": "60 minutes",
        "slots_remaining": equipment.available_slots,
        "usage_instructions": equipment.instructions,
        "reservation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "confirmation_code": f"EQ{random.randint(1000, 9999)}",
        "customer_info": {
            "name": booking.user_name if booking else "John Doe",
            "email": booking.user_email if booking else "john@example.com"
        }
    }
    
    logger.info(f"Equipment reserved successfully: {reservation_id}")
    return reservation_details

@app.post("/api/subscribe/{plan_id}", tags=["Memberships"])
async def subscribe_plan(plan_id: int, booking: Optional[BookingRequest] = None):
    """Subscribe to a membership plan"""
    logger.info(f"Membership subscription requested for plan ID: {plan_id}")
    
    plan = next((p for p in MEMBERSHIPS if p.id == plan_id), None)
    if not plan:
        raise HTTPException(status_code=404, detail="Membership plan not found")
    
    subscription_id = f"SUB-{plan_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    start_date = datetime.now()
    end_date = start_date + timedelta(days=30)  # Monthly subscription
    
    subscription_details = {
        "message": f"Welcome to Elite Fitness {plan.name} membership!",
        "subscription_id": subscription_id,
        "plan_name": plan.name,
        "plan_description": plan.description,
        "monthly_price": f"${plan.price}",
        "duration": plan.duration,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "next_billing_date": end_date.strftime("%Y-%m-%d"),
        "features_included": plan.features,
        "max_guests": plan.max_guests,
        "personal_training_sessions": plan.personal_training_sessions,
        "membership_card": f"Card will be ready for pickup in 24-48 hours",
        "subscription_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "confirmation_code": f"MB{random.randint(1000, 9999)}",
        "welcome_package": "Includes gym tour, fitness assessment, and starter kit",
        "customer_info": {
            "name": booking.user_name if booking else "John Doe",
            "email": booking.user_email if booking else "john@example.com"
        }
    }
    
    logger.info(f"Membership subscription successful: {subscription_id}")
    return subscription_details

# ===============================
# Additional Endpoints
# ===============================

@app.post("/api/contact", tags=["Contact"])
async def submit_contact_form(contact: ContactRequest):
    """Submit contact form"""
    logger.info(f"Contact form submitted by: {contact.email}")
    
    # In a real application, you would send email, save to database, etc.
    ticket_id = f"TICKET-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    return {
        "message": "Thank you for contacting Elite Fitness! We'll get back to you soon.",
        "ticket_id": ticket_id,
        "estimated_response_time": "Within 24 hours",
        "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "contact_info": {
            "phone": "(555) 123-4567",
            "email": "info@elitefitness.com",
            "hours": "Mon-Fri: 6 AM - 10 PM, Sat-Sun: 7 AM - 8 PM"
        }
    }

@app.get("/api/schedule", tags=["Schedule"])
async def get_schedule(date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format")):
    """Get daily schedule of classes and trainer availability"""
    target_date = date if date else datetime.now().strftime("%Y-%m-%d")
    
    schedule = {
        "date": target_date,
        "classes": [
            {
                "time": c.time,
                "name": c.name,
                "instructor": c.instructor,
                "available_spots": c.available_spots,
                "location": c.location
            } for c in CLASSES
        ],
        "trainer_availability": [
            {
                "name": t.name,
                "available_slots": t.available_slots,
                "specialty": t.specialty
            } for t in TRAINERS if t.available_slots
        ],
        "peak_hours": ["6-8 AM", "12-1 PM", "5-7 PM"],
        "recommended_times": ["9-11 AM", "2-4 PM", "8-9 PM"]
    }
    
    return schedule

@app.get("/api/analytics/popular", tags=["Analytics"])
async def get_popular_items():
    """Get most popular classes, trainers, and equipment"""
    return {
        "popular_classes": [
            {"name": "HIIT Inferno", "bookings": 45, "rating": 4.9},
            {"name": "CrossFit Elite", "bookings": 38, "rating": 4.7},
            {"name": "Zen Flow Yoga", "bookings": 32, "rating": 4.8}
        ],
        "popular_trainers": [
            {"name": "Sarah Johnson", "bookings": 52, "rating": 4.9},
            {"name": "Emma Davis", "bookings": 47, "rating": 4.9},
            {"name": "Tony Rodriguez", "bookings": 41, "rating": 4.9}
        ],
        "popular_equipment": [
            {"name": "Treadmill", "usage_hours": 156, "location": "Cardio Zone A"},
            {"name": "Dumbbells", "usage_hours": 142, "location": "Free Weights Zone"},
            {"name": "Cable Machine", "usage_hours": 128, "location": "Strength Training Zone"}
        ],
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.post("/api/analytics/{action}", tags=["Analytics"])
async def track_analytics(action: str, data: Dict[str, Any] = None):
    """Track user analytics and interactions"""
    logger.info(f"Analytics tracked: {action}")
    
    return {
        "message": f"Analytics event '{action}' tracked successfully",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "data": data or {}
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "your-api-is-healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "3.1.0",
        "uptime": "99.9%",
        "database": "connected",
        "services": {
            "classes": "operational",
            "trainers": "operational", 
            "equipment": "operational",
            "bookings": "operational"
        }
    }

# ===============================
# Error Handlers
# ===============================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Resource not found",
            "message": "The requested resource could not be found",
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "timestamp": datetime.now().isoformat()
        }
    )

# ===============================
# Startup Event
# ===============================

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Elite Fitness API v3.1 is starting up...")
    logger.info(f"📊 Loaded {len(CLASSES)} classes")
    logger.info(f"👨‍💼 Loaded {len(TRAINERS)} trainers")
    logger.info(f"🏋️ Loaded {len(EQUIPMENT)} equipment items")
    logger.info(f"💳 Loaded {len(MEMBERSHIPS)} membership plans")
    logger.info("✅ Elite Fitness API is ready!")

# ===============================
# Main
# ===============================

if __name__ == "__main__":
    print("🏋️‍♂️ Starting Elite Fitness API Server...")
    print("📚 API Documentation: http://localhost:8030/docs")
    print("🔍 Alternative Docs: http://localhost:8030/redoc")
    print("📊 API Status: http://localhost:8030")
    print("💪 Health Check: http://localhost:8030/health")
    print("=" * 50)
    
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8030, 
        reload=True,
        log_level="info"
    )
