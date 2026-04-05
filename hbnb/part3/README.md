# HBnB Evolution – Part 3: Authentication and Database Integration
 
## Overview
 
Part 3 focuses on upgrading the HBnB backend by introducing authentication, authorization, and persistent database storage. In this phase, the project moves beyond the in-memory architecture used in previous parts and adopts a more realistic backend design using SQLAlchemy and SQLite.
 
This part also introduces secure password hashing, JWT-based authentication, protected routes, administrator privileges, database modeling, and entity relationships between the core resources of the application.
 
---
 
## Objectives
 
The main objectives of Part 3 are to:
 
- improve the security of the application
- introduce token-based authentication
- enforce authorization rules for protected actions
- replace temporary in-memory storage with persistent database storage
- map application entities to relational database models
- document the database structure using diagrams and SQL scripts
 
---
 
## Part 3 Scope
 
This part includes the following enhancements:
 
- application configuration through the Flask application factory
- password hashing with bcrypt
- JWT authentication with protected endpoints
- role-based authorization for users and administrators
- SQLAlchemy integration for database persistence
- SQLite support for development
- ORM mapping for core entities
- relationship mapping between models
- SQL scripts for schema creation and initial data
- ER diagram documentation using Mermaid.js
 
---
 
## Main Features
 
### Authentication
- Secure password hashing before storing user credentials
- Login endpoint that returns a JWT access token
- Token-based authentication for protected API routes
 
### Authorization
- Users can only update or delete resources they own
- Admin users have elevated permissions for privileged operations
- Public endpoints remain accessible where appropriate
 
### Database Integration
- SQLAlchemy replaces in-memory repositories
- Persistent storage is introduced for application data
- Models are mapped to relational database tables
 
### Data Modeling
The following entities are integrated into the database layer:
 
- User
- Place
- Review
- Amenity
 
Relationships between these entities are also defined to reflect the application domain more accurately.
 
---
 
## Getting Started
 
### Clone the repository and navigate to Part 3
```markdown
git clone https://github.com/Modi-01/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part3
```

 
### Create and activate a virtual environment
```markdown
python3 -m venv venv
source venv/bin/activate
```
 
### Install dependencies
```markdown
pip install -r requirements.txt
```
 
### Configure the application
 
Before running the project, make sure the configuration includes the required settings for authentication and database access.
Configuration values include:
 
- SECRET_KEY
- JWT_SECRET_KEY
- SQLALCHEMY_DATABASE_URI
- SQLALCHEMY_TRACK_MODIFICATIONS
 
### Initialize the database
```markdown
flask db upgrade
```

 
### Run the application
```markdown
flask run
```

### Start testing the API
- user registration
- login and token generation
- protected endpoints
- admin-only endpoints
- CRUD operations for places and reviews
 
## Outcomes
 
The project evolved from a basic backend into a more complete and secure system that supports:
 
- user authentication
- protected API access
- role-based authorization
- persistent database storage
- relational data modeling
- documented schema design
