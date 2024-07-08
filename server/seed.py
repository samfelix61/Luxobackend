from app import app, db
from models import User, CarOwner, Car, Review, Booking, Feature
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

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
        phone_number='1234567890',
        email_confirmed=True
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
        phone_number='0987654321',
        email_confirmed=True
    )
    db.session.add(regular_user)

    # Create some features
    feature_names = ['GPS', 'Air Conditioning', 'Heated Seats', 'Bluetooth']
    for name in feature_names:
        feature = Feature(name=name)
        db.session.add(feature)

    db.session.commit()
