from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

class User(db.Model, SerializerMixin):
    _tablename_ = "users"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'user', name='user_roles'), nullable=False)
    profile_image = db.Column(db.String(255), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    bookings = db.relationship('Booking', backref='user', lazy=True)

    serialize_rules = ('-password', '-reviews.user', '-bookings.user')

    def _repr_(self):
        return f"<User {self.name}>"


class CarOwner(db.Model, SerializerMixin):
    _tablename_ = "car_owners"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    profile_image = db.Column(db.String(255), nullable=True)
    cars = db.relationship('Car', backref='car_owner', lazy=True)

    def _repr_(self):
        return f"<CarOwner {self.name}>"


class Car(db.Model, SerializerMixin):
    _tablename_ = "cars"

    id = db.Column(db.BigInteger, primary_key=True)
    make = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price_per_day = db.Column(db.Numeric, nullable=False)
    availability_status = db.Column(db.Boolean, nullable=False, default=True)
    car_image_url = db.Column(db.String(255), nullable=True)
    owner_id = db.Column(db.BigInteger, db.ForeignKey('car_owners.id'), nullable=False)
    reviews = db.relationship('Review', backref='car', lazy=True)
    bookings = db.relationship('Booking', backref='car', lazy=True)

    def _repr_(self):
        return f"<Car {self.make} {self.model} ({self.year})>"


class Review(db.Model, SerializerMixin):
    _tablename_ = "reviews"

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    car_id = db.Column(db.BigInteger, db.ForeignKey('cars.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)

    def _repr_(self):
        return f"<Review {self.rating} by User {self.user_id} for Car {self.car_id}>"


class Booking(db.Model, SerializerMixin):
    _tablename_ = "bookings"

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    car_id = db.Column(db.BigInteger, db.ForeignKey('cars.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    car_owner_id = db.Column(db.BigInteger, nullable=False)

    def _repr_(self):
        return f"<Booking {self.id} by User {self.user_id} for Car {self.car_id}>"