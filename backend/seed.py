from app import app, db
from models import User, CarOwner, Car, Review, Booking
from flask_bcrypt import Bcrypt
from faker import Faker
from datetime import datetime, timedelta

# Initialize extensions
bcrypt = Bcrypt(app)
fake = Faker()

with app.app_context():
    db.create_all()

    # Create an admin user
    admin_password = bcrypt.generate_password_hash('adminpassword').decode('utf-8')
    admin_user = User(
        name='Admin User',
        email='admin@example.com',
        password=admin_password,
        role='admin',
        profile_image=None,
        phone_number='1234567890'
    )
    db.session.add(admin_user)

    # Create a regular user
    user_password = bcrypt.generate_password_hash('userpassword').decode('utf-8')
    regular_user = User(
        name='Regular User',
        email='user@example.com',
        password=user_password,
        role='user',
        profile_image=None,
        phone_number='0987654321'
    )
    db.session.add(regular_user)

    # Create some fake car owners
    for _ in range(5):
        car_owner = CarOwner(
            name=fake.name(),
            phone_number=fake.phone_number(),
            profile_image=None
        )
        db.session.add(car_owner)

        # Create cars for each car owner
        for _ in range(3):
            car = Car(
                make=fake.company(),
                model=fake.vehicle_model(),
                year=fake.year(),
                price_per_day=fake.random_int(min=50, max=300),
                availability_status=True,
                owner_id=car_owner.id
            )
            db.session.add(car)

    db.session.commit()

    print("Database seeded successfully.")
