# HBnB – Part 2 (API + Validation + Testing)

Part 2 focuses on exposing the HBnB features through a REST API built with **Flask-RESTx**, adding **basic validation**, and documenting/testing the endpoints (Swagger + cURL + unit tests).

---

## Table of Contents

- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run)
- [Swagger Documentation](#swagger-documentation)
- [API Endpoints](#api-endpoints)
  - [Users](#users)
  - [Amenities](#amenities)
  - [Places](#places)
  - [Reviews](#reviews)
- [Validation Rules](#validation-rules)
- [Testing](#testing)
  - [Run Unit Tests](#run-unit-tests)
  - [Manual Testing with cURL](#manual-testing-with-curl)
- [Notes / Known Behaviors](#notes--known-behaviors)

---

## Tech Stack

- Python 3
- Flask
- Flask-RESTx (Swagger/OpenAPI + request validation)
- In-memory repository (no DB in Part 2)

Dependencies are listed in `requirements.txt`.

---

## Project Structure

```
part2/
├─ app/
│  ├─ api/
│  │  ├─ __init__.py              # Flask app factory (Swagger at /api/v1/)
│  │  └─ v1/
│  │     ├─ __init__.py           # Register namespaces
│  │     ├─ users.py              # /api/v1/users
│  │     ├─ amenities.py          # /api/v1/amenities
│  │     ├─ places.py             # /api/v1/places
│  │     └─ reviews.py            # /api/v1/reviews
│  ├─ models/
│  │  ├─ base_model.py
│  │  ├─ user.py
│  │  ├─ amenity.py
│  │  ├─ place.py
│  │  └─ review.py
│  ├─ persistence/
│  │  └─ repository.py            # InMemoryRepository
│  └─ services/
│     ├─ facade.py                # HBnBFacade (business logic)
│     └─ __init__.py              # global facade instance
├─ tests/
│  └─ test_users.py               # Unit tests for Users endpoints
├─ config.py
├─ requirements.txt
└─ run.py                          # Run the API server
```

---

## How to Run

### 1) Create a virtual environment (recommended)

**Windows (CMD/PowerShell)**
```bash
py -m venv .venv
.venv\Scripts\activate
```

**Linux/macOS**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Start the server

From the `part2/` directory:

```bash
python run.py
```

The API will run on:

- `http://127.0.0.1:5000`

---

## Swagger Documentation

Flask-RESTx generates Swagger UI automatically.

Open:

- `http://127.0.0.1:5000/api/v1/`

Use it to:
- inspect request/response formats
- try endpoints in the browser
- verify required fields and models

---

## API Endpoints

Base path: `http://127.0.0.1:5000/api/v1/`

### Users

- `GET /users/` → list all users
- `POST /users/` → create user
- `GET /users/<user_id>` → get a user by id
- `PUT /users/<user_id>` → update a user

**Create user (POST /users/)**
```json
{
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "jane.doe@example.com"
}
```

### Amenities

- `GET /amenities/` → list all amenities
- `POST /amenities/` → create amenity
- `GET /amenities/<amenity_id>` → get amenity by id
- `PUT /amenities/<amenity_id>` → update amenity

**Create amenity (POST /amenities/)**
```json
{
  "name": "WiFi"
}
```

### Places

- `GET /places/` → list all places
- `POST /places/` → create place
- `GET /places/<place_id>` → get place by id
- `PUT /places/<place_id>` → update place
- `GET /places/<place_id>/reviews` → list place reviews

**Create place (POST /places/)**
```json
{
  "title": "My Apartment",
  "description": "Nice place",
  "price": 150,
  "latitude": 24.7136,
  "longitude": 46.6753,
  "owner_id": "<USER_ID>",
  "amenities": ["<AMENITY_ID>"]
}
```

### Reviews

- `GET /reviews/` → list all reviews
- `POST /reviews/` → create review
- `GET /reviews/<review_id>` → get review by id
- `PUT /reviews/<review_id>` → update review (text/rating)
- `DELETE /reviews/<review_id>` → delete review

**Create review (POST /reviews/)**
```json
{
  "text": "Great place!",
  "rating": 5,
  "user_id": "<USER_ID>",
  "place_id": "<PLACE_ID>"
}
```

---

## Validation Rules

Validation is handled across:
- Flask-RESTx models (`@api.expect(..., validate=True)`) for required fields/types
- additional checks in endpoints and the business layer (facade/models)

### User
- `first_name`, `last_name`, `email` are required and must be non-empty strings
- `email` must match a basic email format
- duplicate emails are rejected

### Amenity
- `name` is required and must be a non-empty string

### Place
- requires: `title`, `price`, `latitude`, `longitude`, `owner_id`
- owner must exist
- if `amenities` list is provided, each amenity id must exist

### Review
- `text` must be a non-empty string
- `user_id` must reference an existing user
- `place_id` must reference an existing place
- one review per user per place (duplicate review is rejected)

---

## Testing

### Run Unit Tests

Unit tests are located under `tests/`.

From the `part2/` directory:

**Run all tests**
```bash
python -m unittest discover -s tests
```

**Run a specific file**
```bash
python -m unittest tests/test_users.py
```

> Note: tests use Flask's `test_client()` and do **not** require the server to be running.

### Manual Testing with cURL

You can test endpoints manually using cURL.

**Create a user**
```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"John","last_name":"Doe","email":"john.doe@example.com"}'
```

**Duplicate email (should fail)**
```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"John","last_name":"Doe","email":"john.doe@example.com"}'
```

**Swagger-based testing**
- Open `http://127.0.0.1:5000/api/v1/`
- Try requests directly from the UI

---

## Notes / Known Behaviors

- Part 2 uses an **in-memory repository** (`InMemoryRepository`). Data resets when the Python process stops.
- Error messages/status codes are designed to follow the requirements of Part 2 and the unit tests.


