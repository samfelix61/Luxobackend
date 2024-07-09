from app import app, db
from models import User, CarOwner, Car, Review, Booking

with app.app_context():
    # Drop all existing tables
    db.drop_all()

    # Create all tables
    db.create_all()

    # Create sample data
    user1 = User(
        name="John Doe",
        email="john.doe@example.com",
        password="hashed_password_1",  # Ensure passwords are hashed as per your app logic
        role="user",
        profile_image=None,
        phone_number="1234567890"
    )

    user2 = User(
        name="Jane Smith",
        email="jane.smith@example.com",
        password="hashed_password_2",  # Ensure passwords are hashed as per your app logic
        role="admin",
        profile_image=None,
        phone_number="0987654321"
    )

    car_owner = CarOwner(
        name="Car Owner 1",
        phone_number="111222333",
        profile_image=None
    )

    car = Car(
        make="Toyota",
        model="Camry",
        year=2020,
        price_per_day=50,
        availability_status=True,
        car_image_url=None,
        owner_id=1  # Ensure this matches the actual owner_id after creation
    )

    review = Review(
        user_id=1,  # Ensure this matches the actual user_id after creation
        car_id=1,   # Ensure this matches the actual car_id after creation
        rating=5,
        comment="Great car!"
    )

    booking = Booking(
        user_id=1,  # Ensure this matches the actual user_id after creation
        car_id=1,   # Ensure this matches the actual car_id after creation
        start_date="2023-07-10",
        end_date="2023-07-15",
        car_owner_id=1  # Ensure this matches the actual car_owner_id after creation
    )

    # Add to session
    db.session.add_all([user1, user2, car_owner, car, review, booking])
    
    # Commit session
    db.session.commit()

    print("Database seeded!")
