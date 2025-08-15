AUV Fleet Manager

A full-stack Flask web application to manage and simulate control of a fleet of Autonomous Underwater Vehicles (AUVs). This system enables secure authentication, CRUD operations for AUV records, simulated telemetry feedback, and command interfaces — all built with security, scalability, and real-world deployment practices in mind.

Built For

This project is part of a deeper learning journey exploring python full stack frameworks. It is designed with:

Microservices and containerisation in mind

Backend emphasis using Flask, SQLAlchemy, PostgreSQL

Secure practices (e.g. environment variables, password hashing, login control)

Simulated Command & Control functionality over AUVs

Realistic development structure with Docker & Git-based workflows

Features

Secure user registration and login (hashed passwords, sessions)

RUD operations on AUVs (create, view, update, delete)

AUV "Command Center" to simulate live control

Display of simulated telemetry (depth, temperature, heading)

RESTful API endpoints for integration

HTML templating with Jinja2

Flask Blueprints for modular design

Full Docker support (app + database)

.env-based configuration and secrets management

Git-based versioning and CI-ready structure

🛠 Tech Stack

Layer

Tools/Libraries

Backend

Flask, SQLAlchemy, Flask-Login, Flask-Bcrypt

Frontend

Jinja2, HTML5, Bootstrap (optional)

Database

PostgreSQL

Auth/Security

Bcrypt, Flask-Login, SECRET_KEY

DevOps

Docker, Docker Compose, .env, Git

Migration

Flask-Migrate, Alembic

Getting Started

Prerequisites

Docker & Docker Compose

Python 3.12+

pip, virtualenv (for local running)

Git

Run with Docker

Clone the repository

git clone https://github.com/yourusername/auv-fleet-manager.git
cd auv-fleet-manager

Create .env file

SECRET_KEY=supersecurekey
DB_USER=user
DB_PASSWORD=password
DB_NAME=auv_db

Start containers

docker compose up --build

Visit

http://localhost:5000

Run Locally (without Docker)

Create virtualenv

python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

Install dependencies

pip install -r requirements.txt

Set environment

export FLASK_APP=app
export FLASK_ENV=development

Initialize DB

flask db init
flask db migrate -m "Initial"
flask db upgrade

Run

flask run

Project Structure

auv-fleet-manager/
│
├── app/                        # Application package
│   ├── __init__.py             # App factory, DB config
│   ├── models.py               # SQLAlchemy models
│   ├── routes.py               # Blueprints & views
│   ├── templates/              # HTML templates
│   ├── static/                 # JS, CSS
│   └── ...                     
│
├── migrations/                 # Flask-Migrate/Alembic files
├── Dockerfile                  # Flask app image
├── docker-compose.yml          # App + DB services
├── requirements.txt
├── .env                        # Not committed to Git
└── README.md

🔐 Security Features

Passwords hashed using Bcrypt

Login sessions protected via Flask-Login

Environment variables hide credentials

@login_required decorators on protected routes

Input validation on all forms and JSON routes

🧪 Testing

Basic testing structure planned for:

API endpoint responses

User registration/login flows

Auth-protected route access

Testing stack may include pytest and Flask-Testing module (future roadmap).

🌟 Roadmap



📚 Learning Goals Met

Flask Blueprints, ORM, sessions

Secure authentication (login manager, hashed passwords)

Docker fundamentals (Dockerfile, docker-compose)

SQLAlchemy ORM + Alembic migrations

Template rendering and form handling

Simulating a realistic Command & Control interface

🏁 Credits

This project is part of a hands-on upskilling and career transition effort by [Your Name], and was designed to demonstrate:

Engineering understanding of web backends

Realistic software project development

Readiness for roles like C2 Software Engineer at the National Oceanography Centre
