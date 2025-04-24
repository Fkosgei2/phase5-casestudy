from models import db, User, TrainingProgram, Payment, Booking, BlogPost, Testimonial, CaseStudy, ContactUs
from datetime import datetime
from werkzeug.security import generate_password_hash
from app import app as create_app  # Import the app factory or app instance

# Create sample users dynamically, checking for duplicates
def create_sample_users():
    users_to_create = [
        {"full_name": "Kipngetich Kosgei", "email": "kk@gmail.com", "password": "password123", "phone_number": "0711211446"},
        {"full_name": "Amar Find", "email": "amarmoringa@egmail.com", "password": "password456", "phone_number": "07987654321"}
    ]

    for user_data in users_to_create:
        existing_user = User.query.filter_by(full_name=user_data["full_name"]).first()
        if not existing_user:
            user = User(
                full_name=user_data["full_name"],
                email=user_data["email"],
                password=generate_password_hash(user_data["password"]),
                phone_number=user_data["phone_number"]
            )
            db.session.add(user)
        else:
            print(f"User '{user_data['full_name']}' already exists. Skipping...")

    db.session.commit()

# Create sample training programs
def create_sample_training_programs():
    if TrainingProgram.query.count() > 0:
        print("Training programs already exist. Skipping...")
        return

    program1 = TrainingProgram(
        title="SIYB Training",
        description="Entrepreneurship training for youth.",
        category="SIYB_training"
    )
    program2 = TrainingProgram(
        title="Data Analytics Workshop",
        description="Hands-on training in data analysis using Python.",
        category="Data_Analytics"
    )

    db.session.add_all([program1, program2])
    db.session.commit()

# Create sample bookings
def create_sample_bookings():
    user = User.query.first()
    program = TrainingProgram.query.first()
    if not user or not program:
        print("Missing user or training program. Skipping booking creation.")
        return

    if not Booking.query.first():
        booking = Booking(
            user_id=user.id,
            training_program_id=program.id,
            status="confirmed",
            notes="Looking forward to the training."
        )
        db.session.add(booking)
        db.session.commit()

# Create sample payments
def create_sample_payments():
    user = User.query.first()
    program = TrainingProgram.query.first()
    booking = Booking.query.first()
    if not user or not program or not booking:
        print("Missing required data for payment. Skipping...")
        return

    if not Payment.query.first():
        payment = Payment(
            user_id=user.id,
            booking_id=booking.id,
            training_program_id=program.id,
            amount=100.0,
            payment_method="Credit Card",
            payment_status="completed",
            transaction_id="txn123"
        )
        db.session.add(payment)
        db.session.commit()

# Create sample blog posts
def create_sample_blog_posts():
    user = User.query.first()
    if not user:
        return

    if not BlogPost.query.first():
        blog_post = BlogPost(
            author_id=user.id,
            body="This is a sample blog post about entrepreneurship.",
            image="sample_image.jpg"
        )
        db.session.add(blog_post)
        db.session.commit()

# Create sample testimonials
def create_sample_testimonials():
    if not Testimonial.query.first():
        testimonial = Testimonial(
            client_name="Alice Johnson",
            media="video.mp4",
            business_reference="TechCorp",
            approval_status="approved"
        )
        db.session.add(testimonial)
        db.session.commit()

# Create sample case studies
def create_sample_case_studies():
    if not CaseStudy.query.first():
        case_study = CaseStudy(
            title="Success Story: TechCorp's Growth",
            summary="A case study about the rapid growth of TechCorp.",
            type="Research",
            results="TechCorp increased revenue by 50%.",
            media="success_story.pdf"
        )
        db.session.add(case_study)
        db.session.commit()

# Create sample contact us entries
def create_sample_contact_us():
    if not ContactUs.query.first():
        contact = ContactUs(
            name="Samuel Peters",
            email="samuel.peters@example.com",
            message="I would like more information about your services.",
            facebook="facebook.com/samuel",
            twitter="twitter.com/samuel"
        )
        db.session.add(contact)
        db.session.commit()

# Main seeding function
def seed_data():
    with app.app_context():
        db.create_all()

        create_sample_users()
        create_sample_training_programs()
        create_sample_bookings()
        create_sample_payments()
        create_sample_blog_posts()
        create_sample_testimonials()
        create_sample_case_studies()
        create_sample_contact_us()

        print("Database seeded successfully!")

# Entry point
if __name__ == "__main__":
    app = create_app
    app.app_context().push()
    seed_data()
