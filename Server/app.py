from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, User, TrainingProgram, Booking, Payment




# Configurations
def create():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///training.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app
# Initialize Flask-Migrate and extension
app = create()
db.init_app(app)
migrate = Migrate(app, db)
migrate = Migrate(app, db)
CORS(app)
# Routes

@app.route('/')
def index():
    return {"message": "Welcome to Training Program API"}

# User Routes
@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])
    elif request.method == 'POST':
        data = request.get_json()
        new_user = User(
            full_name=data['full_name'],
            email=data['email'],
            password=data['password'],  # Make sure to hash in real apps!
            phone_number=data['phone_number']
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201

# TrainingProgram Routes
@app.route('/programs', methods=['GET', 'POST'])
def handle_programs():
    if request.method == 'GET':
        programs = TrainingProgram.query.all()
        return jsonify([program.to_dict() for program in programs])
    elif request.method == 'POST':
        data = request.get_json()
        new_program = TrainingProgram(
            title=data['title'],
            description=data['description'],
            category=data['category']
        )
        db.session.add(new_program)
        db.session.commit()
        return jsonify(new_program.to_dict()), 201

# Booking Routes
@app.route('/bookings', methods=['GET', 'POST'])
def handle_bookings():
    if request.method == 'GET':
        bookings = Booking.query.all()
        return jsonify([booking.to_dict() for booking in bookings])
    elif request.method == 'POST':
        data = request.get_json()
        new_booking = Booking(
            user_id=data['user_id'],
            training_program_id=data['training_program_id'],
            status=data.get('status', 'pending'),
            notes=data.get('notes')
        )
        db.session.add(new_booking)
        db.session.commit()
        return jsonify(new_booking.to_dict()), 201

# Payment Routes
@app.route('/payments', methods=['GET', 'POST'])
def handle_payments():
    if request.method == 'GET':
        payments = Payment.query.all()
        return jsonify([payment.to_dict() for payment in payments])
    elif request.method == 'POST':
        data = request.get_json()
        new_payment = Payment(
            user_id=data['user_id'],
            booking_id=data['booking_id'],
            training_program_id=data['training_program_id'],
            amount=data['amount'],
            payment_method=data['payment_method'],
            payment_status=data.get('payment_status', 'pending'),
            transaction_id=data['transaction_id']
        )
        db.session.add(new_payment)
        db.session.commit()
        return jsonify(new_payment.to_dict()), 201

# Run App
if __name__ == '__main__':
    app.run(debug=True)
