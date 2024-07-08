from flask import Flask, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from datetime import timedelta
from models import db, User, CarOwner, Car, Review, Booking, Feature
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///car_rental_platform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# User Registration with Email Confirmation
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

    # Send confirmation email
    token = serializer.dumps(new_user.email, salt='email-confirm')
    confirm_url = url_for('confirm_email', token=token, _external=True)
    # send_email(new_user.email, confirm_url)  # Implement this function to send the email

    return jsonify({'message': 'User registered successfully. Please confirm your email.'}), 201

@app.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        return jsonify({'message': 'The confirmation link expired.'}), 400
    except BadSignature:
        return jsonify({'message': 'Invalid confirmation token.'}), 400

    user = User.query.filter_by(email=email).first_or_404()
    user.email_confirmed = True
    db.session.commit()
    return jsonify({'message': 'Email confirmed successfully.'}), 200

# Password Reset Request
@app.route('/reset_password', methods=['POST'])
def reset_password_request():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'message': 'User not found.'}), 404

    token = serializer.dumps(user.email, salt='password-reset')
    reset_url = url_for('reset_password', token=token, _external=True)
    # send_email(user.email, reset_url)  # Implement this function to send the email

    return jsonify({'message': 'Password reset link sent.'}), 200

@app.route('/reset_password/<token>', methods=['POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset', max_age=3600)
    except SignatureExpired:
        return jsonify({'message': 'The password reset link expired.'}), 400
    except BadSignature:
        return jsonify({'message': 'Invalid password reset token.'}), 400

    data = request.get_json()
    user = User.query.filter_by(email=email).first_or_404()
    hashed_password = bcrypt.generate_password_hash(data['new_password']).decode('utf-8')
    user.password = hashed_password
    db.session.commit()
    return jsonify({'message': 'Password reset successfully.'}), 200

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        if not user.email_confirmed:
            return jsonify({'message': 'Email not confirmed.'}), 403
        access_token = create_access_token(identity={'id': user.id, 'role': user.role}, expires_delta=timedelta(hours=1))
        return jsonify({'access_token': access_token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

# Create Car Feature
@app.route('/features', methods=['POST'])
@jwt_required()
def create_feature():
    data = request.get_json()
    new_feature = Feature(name=data['name'])
    db.session.add(new_feature)
    db.session.commit()
    return jsonify({'message': 'Feature created successfully'}), 201

# Get All Features
@app.route('/features', methods=['GET'])
def get_features():
    features = Feature.query.all()
    return jsonify([{'id': feature.id, 'name': feature.name} for feature in features])

if __name__ == "__main__":
    app.run(debug=True)
