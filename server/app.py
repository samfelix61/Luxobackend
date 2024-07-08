from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from datetime import timedelta
from models import db, User, CarOwner, Car, Review, Booking

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///car_rental_platform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
db.init_app(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(
        name=data['name'],
        email=data['email'],
        password=hashed_password,
        role=data['role'],
        profile_image=data.get('profile_image'),
        phone_number=data.get('phone_number')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'id': user.id, 'role': user.role}, expires_delta=timedelta(hours=1))
        return jsonify({'access_token': access_token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

# Create User Profile
@app.route('/profile', methods=['POST'])
@jwt_required()
def create_profile():
    data = request.get_json()
    user_id = get_jwt_identity()['id']
    user = User.query.get(user_id)
    user.profile_image = data.get('profile_image')
    user.phone_number = data.get('phone_number')
    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'})

# Get User Profile
@app.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()['id']
    user = User.query.get(user_id)
    return jsonify({
        'name': user.name,
        'email': user.email,
        'role': user.role,
        'profile_image': user.profile_image,
        'phone_number': user.phone_number
    })

# Create Car Hire
@app.route('/car_hires', methods=['POST'])
@jwt_required()
def create_car_hire():
    data = request.get_json()
    user_id = get_jwt_identity()['id']
    new_booking = Booking(
        user_id=user_id,
        car_id=data['car_id'],
        start_date=data['start_date'],
        end_date=data['end_date'],
        car_owner_id=data['car_owner_id']
    )
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({'message': 'Car hire created successfully'}), 201

# Get Car Hires
@app.route('/car_hires', methods=['GET'])
@jwt_required()
def get_car_hires():
    car_hires = Booking.query.all()
    return jsonify([{
        'id': hire.id,
        'user_id': hire.user_id,
        'car_id': hire.car_id,
        'start_date': hire.start_date,
        'end_date': hire.end_date,
        'car_owner_id': hire.car_owner_id
    } for hire in car_hires])

# CRUD for Reviews
@app.route('/reviews', methods=['POST'])
@jwt_required()
def create_review():
    data = request.get_json()
    user_id = get_jwt_identity()['id']
    new_review = Review(
        user_id=user_id,
        car_id=data['car_id'],
        rating=data['rating'],
        comment=data['comment']
    )
    db.session.add(new_review)
    db.session.commit()
    return jsonify({'message': 'Review created successfully'}), 201

@app.route('/reviews/<int:id>', methods=['GET'])
def get_review(id):
    review = Review.query.get_or_404(id)
    return jsonify({
        'user_id': review.user_id,
        'car_id': review.car_id,
        'rating': review.rating,
        'comment': review.comment
    })

@app.route('/reviews/<int:id>', methods=['PUT'])
@jwt_required()
def update_review(id):
    data = request.get_json()
    review = Review.query.get_or_404(id)
    review.rating = data['rating']
    review.comment = data['comment']
    db.session.commit()
    return jsonify({'message': 'Review updated successfully'})

@app.route('/reviews/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_review(id):
    review = Review.query.get_or_404(id)
    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Review deleted successfully'})

# Admin Role
@app.route('/admin/car_hires', methods=['GET'])
@jwt_required()
def admin_get_car_hires():
    claims = get_jwt_identity()
    if claims['role'] != 'admin':
        return jsonify({'message': 'Admins only!'}), 403
    car_hires = Booking.query.all()
    return jsonify([{
        'id': hire.id,
        'user_id': hire.user_id,
        'car_id': hire.car_id,
        'start_date': hire.start_date,
        'end_date': hire.end_date,
        'car_owner_id': hire.car_owner_id
    } for hire in car_hires])

if __name__ == "__main__":
    app.run(debug=True)
