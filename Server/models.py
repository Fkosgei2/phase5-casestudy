from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import MetaData, Enum
from enum import Enum as PyEnum
from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, SelectField,
    HiddenField, DateTimeField, SubmitField
    )
from wtforms.validators import DataRequired, Optional
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Naming conventions for constraints
metadata = MetaData(naming_convention={
    "pk": "pk_%(table_name)s_%(column_0_name)s",
    "ix": "ix_%(table_name)s_%(column_0_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "tab": "tab_%(table_name)s",
})

# Initialize SQLAlchemy
db = SQLAlchemy(metadata=metadata)

# Enum for categories
class Category(PyEnum):
    SIYB_training = "SIYB training"
    Data_Analytics = "Data Analytics"
    Monitoring_and_Evaluation = "Monitoring and Evaluation"
    Research = "Research"

# User Model
class User(db.Model, SerializerMixin):
    __tablename__ = "users"
    serialize_rules = ( '-created_at', '-password', '-bookings.user', '-payments.user',
                       '-blog_posts.author', '-blog_comments.user', '-testimonials.user',
                       '-contact_us.user', '-newsletter_subscriptions.user',
                       '-case_studies.author', '-faqs.user')

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)   
    phone_number = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    payments = db.relationship('Payment', back_populates='user', cascade="all, delete-orphan")
    blog_posts = db.relationship('BlogPost', back_populates='author', cascade="all, delete-orphan")

    # def validate_password(self, password):
    #     """
    #     Validate the password against certain criteria.
    #     :param password: The password to validate.
    #     :return: True if valid, False otherwise.
    #     """
    #     if len(password) < 8:
    #         return False
    #     if not any(char.isdigit() for char in password):
    #         return False
    #     if not any(char.isalpha() for char in password):
    #         return False
    #     if not any(char in "!@#$%^&*()-_+=<>?" for char in password):
    #         return False
    #     return True
    # def __init__(self, full_name, email, password, phone_number):
    #     self.full_name = full_name
    #     self.email = email
    #     self.password = password  # Make sure to hash in real apps!
    #     self.phone_number = phone_number
    #     self.created_at = datetime.utcnow()
    #     # Add your password validation logic here
        

# Training Program Model
class TrainingProgram(db.Model, SerializerMixin):
    __tablename__ = "training_programs"
    serialize_rules = ('-bookings.training_program', '-payments.training_program',
                       '-case_studies.training_program')

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(Enum(Category, name='training_category_type'), nullable=False)

    payments = db.relationship('Payment', back_populates='training_program', cascade="all, delete-orphan")

# Payment Model
class Payment(db.Model, SerializerMixin):
    __tablename__ = "payments"
    serialize_rules = ('-user.payments', '-training_program.payments', '-booking.payments')

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    training_program_id = db.Column(db.Integer, db.ForeignKey('training_programs.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    payment_method = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(50), nullable=False, default='pending')
    transaction_id = db.Column(db.String(100), unique=True, nullable=False)

    user = db.relationship('User', back_populates='payments')
    training_program = db.relationship('TrainingProgram', back_populates='payments')

  
class Booking(db.Model):
    __tablename__ = 'bookings'
    serialize_rules = ()
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    training_program_id = db.Column(db.Integer, db.ForeignKey('training_programs.id'), nullable=False)
    status = db.Column(db.String(50), default='pending')
    notes = db.Column(db.String(255))

    user = db.relationship('User', backref='bookings')
    training_program = db.relationship('TrainingProgram', backref='bookings')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'training_program_id': self.training_program_id,
            'status': self.status,
            'notes': self.notes
        }


# Blog Post Model
class BlogPost(db.Model, SerializerMixin):
    __tablename__ = "blog_posts"
    serialize_rules = ('-author.blog_posts', '-comments.blog_post')

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    date_published = db.Column(db.DateTime, default=db.func.current_timestamp())
    image = db.Column(db.String(200), nullable=True)

    author = db.relationship('User', back_populates='blog_posts')

# Testimonial Model
class Testimonial(db.Model, SerializerMixin):
    __tablename__ = "testimonials"
    serialize_rules = ('-user.testimonials',)

    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    media = db.Column(db.String(200), nullable=False)
    business_reference = db.Column(db.String(100), nullable=False)
    approval_status = db.Column(db.String(50), nullable=False, default='pending')


# Case Study Model
class CaseStudy(db.Model, SerializerMixin):
    __tablename__ = "case_studies"
    serialize_rules = ('-author.case_studies',)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    type = db.Column(Enum(Category, name='case_study_type'), nullable=False)
    results = db.Column(db.Text, nullable=False)
    media = db.Column(db.String(200), nullable=True)

# FAQ Form
class FAQForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired()])
    answer = TextAreaField('Answer', validators=[DataRequired()])
    category = SelectField(
        'Category',
        choices=[(category.name, category.value) for category in Category],
        validators=[DataRequired()]
    )
    last_updated = DateTimeField('Last Updated', format='%Y-%m-%d %H:%M', default=datetime.utcnow)

# Contact Us Model
class ContactUs(db.Model, SerializerMixin):
    __tablename__ = "contact_us"
    serialize_rules = ('-user.contact_us',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False, default='pending')

    facebook = db.Column(db.String(100), nullable=True)
    twitter = db.Column(db.String(100), nullable=True)
    linkedin = db.Column(db.String(100), nullable=True)
    instagram = db.Column(db.String(100), nullable=True)
    youtube = db.Column(db.String(100), nullable=True)
    tiktok = db.Column(db.String(100), nullable=True)

    def __init__(self, name, email, message, facebook=None, twitter=None, linkedin=None, instagram=None, youtube=None, tiktok=None):
        self.name = name
        self.email = email
        self.message = message
        self.facebook = facebook
        self.twitter = twitter
        self.linkedin = linkedin
        self.instagram = instagram
        self.youtube = youtube
        self.tiktok = tiktok
        self.created_at = datetime.utcnow()
        self.status = 'pending'
