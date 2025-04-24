# SIYB E-Learning Platform

This project is a Flask-based web application for managing training programs, user bookings, payments, and other related functionalities. It includes models for database management, API routes for interaction, and a seeding script to populate the database with initial data.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Models](#models)
- [API Endpoints](#api-endpoints)
- [Database Seeding](#database-seeding)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
-
---
## Overview

The **SIYB E-Learning Platform** is designed to facilitate training programs for users, 
including features like user registration, program management, bookings, payments, 
and testimonials. It uses Flask for the backend, SQLite for the database, and Flask-Migrate for database migrations.

## Features

- User management (CRUD operations)
- Training program management
- Booking and payment handling
- Blog posts and testimonials
- Database seeding for initial data population
- RESTful API for interaction
---
## Project Structure

SIYB_E-Learning/ 
  ├── Server/
     ├── app.py # Main application and routes  file │
     ├── models.py # Database models │ 
     ├── seed.py # Database seeding script │
     ├── migrations/ # Flask-Migrate migration files │ 
       └── training.db # SQLite database file 
     └── README.md # Project documentation


---

## Models

The `models.py` file defines the database schema using SQLAlchemy. Below are the key models:

### 1. **User**
Represents a user in the system.

- **Fields**:
  - `id`: Primary key
  - `full_name`: Full name of the user
  - `email`: Unique email address
  - `phone_number`: Contact number
  - `password`: Hashed password
  - `created_at`: Timestamp of user creation

- **Relationships**:
  - `payments`: One-to-many relationship with `Payment`
  - `blog_posts`: One-to-many relationship with `BlogPost`

---

### 2. **TrainingProgram**
Represents a training program.

- **Fields**:
  - `id`: Primary key
  - `title`: Title of the program
  - `description`: Description of the program
  - `category`: Enum field for program category

- **Relationships**:
  - `payments`: One-to-many relationship with `Payment`

---

### 3. **Booking**
Represents a booking made by a user for a training program.

- **Fields**:
  - `id`: Primary key
  - `user_id`: Foreign key to `User`
  - `training_program_id`: Foreign key to `TrainingProgram`
  - `status`: Booking status (default: `pending`)
  - `notes`: Additional notes

---

### 4. **Payment**
Represents a payment made by a user.

- **Fields**:
  - `id`: Primary key
  - `user_id`: Foreign key to `User`
  - `booking_id`: Foreign key to `Booking`
  - `training_program_id`: Foreign key to `TrainingProgram`
  - `amount`: Payment amount
  - `payment_method`: Method of payment
  - `payment_status`: Status of payment (default: `pending`)
  - `transaction_id`: Unique transaction ID
---
### 5. **BlogPost**
Represents a blog post authored by a user.

- **Fields**:
  - `id`: Primary key
  - `author_id`: Foreign key to `User`
  - `body`: Content of the blog post
  - `date_published`: Timestamp of publication
  - `image`: Optional image URL
---
### 6. **Testimonial**
Represents a testimonial submitted by a client.

- **Fields**:
  - `id`: Primary key
  - `client_name`: Name of the client
  - `media`: Media file (e.g., video or image)
  - `business_reference`: Reference to the client's business
  - `approval_status`: Status of the testimonial (default: `pending`)
---

## API Endpoints (app.py)

The `app.py` file defines the following RESTful API endpoints:

### 1. **User Routes**
- `GET /users`: Retrieve all users.
- `POST /users`: Create a new user.

### 2. **Training Program Routes**
- `GET /programs`: Retrieve all training programs.
- `POST /programs`: Create a new training program.

### 3. **Booking Routes**
- `GET /bookings`: Retrieve all bookings.
- `POST /bookings`: Create a new booking.

### 4. **Payment Routes**
- `GET /payments`: Retrieve all payments.
- `POST /payments`: Create a new payment.
---
## Database Seeding

The `seed.py` file is used to populate the database with initial data.
It includes functions to create sample users, training programs, bookings, payments, and more.

### Usage:
Run the following command to seed the database:

```bash
python seed.py

Setup and Installation
Prerequisites
Python 3.8 or higher
Flask and related dependencies
Installation Steps
Clone the repository:
  git clone <repository-url>
  cd SIYB_E-Learning/Server

Create a virtual environment:
 python3 pipenv install && pipenv shell

Install dependencies:
  pipenv install (quirements)

Initialize the database:
  flask db init
  flask db migrate -m "Initial migration"
  flask db upgrade

Seed the database:
  python seed.py

Run the application:
  python3 seed.py



