from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import app, db  # Adjust this import as per your actual app structure
from models import User, CarOwner, Car, Review, Booking  # Adjust this import as per your actual models structure

# Create Car Owner
@app.route('/car_owners', methods=['POST'])
@jwt_required()
def create_car_owner():
    data = request.get_json()
    new_car_owner = CarOwner(
        name=data['name'],
        phone_number=data.get('phone_number'),
        profile_image=data.get('profile_image')
    )
    db.session.add(new_car_owner)
    db.session.commit()
    return jsonify({'message': 'Car owner created successfully'}), 201

# Get Car Owners
@app.route('/car_owners', methods=['GET'])
@jwt_required()
def get_car_owners():
    car_owners = CarOwner.query.all()
    return jsonify([{
        'id': owner.id,
        'name': owner.name,
        'phone_number': owner.phone_number,
        'profile_image': owner.profile_image
    } for owner in car_owners])

# Create Car
@app.route('/cars', methods=['POST'])
@jwt_required()
def create_car():
    data = request.get_json()
    new_car = Car(
        make=data['make'],
        model=data['model'],
        year=data['year'],
        price_per_day=data['price_per_day'],
        availability_status=data.get('availability_status', True),
        car_image_url=data.get('car_image_url'),
        owner_id=data['owner_id']
    )
    db.session.add(new_car)
    db.session.commit()
    return jsonify({'message': 'Car created successfully'}), 201

# Get Cars
@app.route('/cars', methods=['GET'])
@jwt_required()
def get_cars():
    cars = Car.query.all()
    return jsonify([{
        'id': car.id,
        'make': car.make,
        'model': car.model,
        'year': car.year,
        'price_per_day': str(car.price_per_day),
        'availability_status': car.availability_status,
        'car_image_url': car.car_image_url,
        'owner_id': car.owner_id
    } for car in cars])

# Other routes such as reviews, bookings, etc. can be similarly defined here

# Example route with JWT authentication
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Not Found'}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'message': 'Internal Server Error'}), 500

# Ensure that this module is executed when running this file directly
if __name__ == '__main__':
    app.run(debug=True)
