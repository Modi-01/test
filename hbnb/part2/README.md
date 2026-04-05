## Part 2 — Implementation of Business Logic and API Endpoints

In this part, the documented design was transformed into a working implementation using **Python**, **Flask**, and **Flask-RESTx**.  
The focus was on building the **Business Logic** and **Presentation (API)** layers, organizing the project in a modular structure, and implementing core RESTful endpoints.

### What was implemented

- **Project setup and package initialization**
  - Organized the codebase into a modular structure.
  - Prepared the project layers (Presentation, Business Logic, and repository-based persistence preparation).
  - Integrated the **Facade pattern** for communication between layers.

- **Core business logic classes**
  - Implemented the main entities:
    - `User`
    - `Place`
    - `Review`
    - `Amenity`
  - Added attributes, methods, and relationships between entities.
  - Implemented validation logic and entity update behavior.

- **API endpoints (Flask / Flask-RESTx)**
  - Implemented RESTful endpoints for:
    - **Users**
    - **Amenities**
    - **Places**
    - **Reviews**
  - Connected endpoints to the Business Logic layer through the Facade.
  - Used **Flask-RESTx** for route organization and API documentation (Swagger).

### CRUD coverage in Part 2

- **Users:** `POST`, `GET`, `PUT` (**DELETE not implemented** in this part)
- **Amenities:** `POST`, `GET`, `PUT` (**DELETE not implemented** in this part)
- **Places:** `POST`, `GET`, `PUT` (**DELETE not implemented** in this part)
- **Reviews:** `POST`, `GET`, `PUT`, `DELETE`

> **Note:** Review is the only entity that includes `DELETE` in Part 2.

### Validation and data handling

- Added basic validation for endpoint inputs and model attributes.
- Ensured correct response formats and status codes.
- Handled entity relationships in API responses (e.g., place-related owner/amenity data as required by the project logic).
- Excluded sensitive fields like passwords from user responses.

### Outcome of Part 2

By completing Part 2, the project now has:

- A clean and modular architecture ready for extension.
- Working business logic classes and relationships.
- Functional REST API endpoints for the core entities.
- Validation and testing coverage for implemented endpoints.
- A strong foundation for **Part 3**, where authentication and database-backed persistence will be added.
