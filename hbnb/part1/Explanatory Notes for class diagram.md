📝 Explanatory Notes
## *User Entity*

The User entity represents the users of the system.
It stores basic user information such as first name, last name, email, and password, along with a flag indicating whether the user is an administrator.

## Key Attributes:

first_name

last_name

email

password

is_admin

### Key Methods:

create()

update()

delete()

This entity contributes to the business logic by allowing users to own places and write reviews.
---

## *Place Entity*

The Place entity represents the properties listed in the application.
Each place is associated with a single user (the owner) and contains descriptive information, pricing, and geographic location.

## Key Attributes:

title

description

price

latitude

longitude

### Key Methods:

create()

update()

delete()

This entity plays a central role in the system by linking users, amenities, and reviews.
---

## *Review Entity*

The Review entity represents reviews written by users about places they have visited.
Each review is associated with one user and one place.

## Key Attributes:

rating

comment

### Key Methods:

create()

update()

delete()

This entity supports user feedback and evaluation of places.
---

## *Amenity Entity*

The Amenity entity represents facilities or features that can be associated with places, such as Wi-Fi or parking.

## Key Attributes:

name

description

### Key Methods:

create()

update()

delete()

This entity allows places to be categorized based on the services they offer.
---

## *BaseModel Entity*

The BaseModel entity is the base class inherited by all other entities.
It provides shared attributes to ensure consistency and traceability across the system.

## Key Attributes:

id (UUID)

created_at

updated_at

---
<img width="1529" height="929" alt="Class digram" src="https://github.com/user-attachments/assets/34de6edd-6194-4a97-85bd-fbfd97bac1da" />




## *🔗 Relationships Between Entities*

User – Place: One-to-Many relationship. A user can own multiple places.

User – Review: One-to-Many relationship. A user can write multiple reviews.

Place – Review: One-to-Many relationship. A place can have multiple reviews.

Place – Amenity: Many-to-Many relationship. A place can have multiple amenities, and an amenity can be associated with multiple places.

All entities inherit from BaseModel to ensure unique identification and audit tracking.
---
