# HBnB Evolution - Technical Documentation
## Introduction
### Purpose of the Document
This document provides a comprehensive technical blueprint for the **HBnB application** project. It describes the system architecture, key design decisions, and interactions between components. The goal is to guide the upcoming implementation phases and serve as a reference for developers.
### Project Overview
HBnB application is a simplified Airbnb-like application that allows users to:
- Register and manage user profiles (regular users and administrators).
- List properties (places) with details such as title, description, price, and location (latitude/longitude).
- Leave reviews (rating and comment) for places.
- Manage amenities that can be associated with places.
- The application follows a **three-layer architecture** and uses a **Facade Pattern** to ensure modularity, maintainability, and separation of concerns.
## High-Level Architecture
### Package Diagram
<img width="1723" height="1416" alt="HBNB PackageDiagram" src="https://github.com/user-attachments/assets/6d862a32-2932-4c59-946d-e438bbc8cdae" />

#### Overview
The system is divided into three layers:
- **Presentation Layer (Services, API)**  
Handles user interactions and exposes API endpoints. It delegates application use-cases to the Business Logic layer through a unified entry point (facade).
- **Business Logic Layer (Models)**  
Contains the core domain entities (User, Place, Review, Amenity) and application rules. It provides a **Facade** that orchestrates use-cases and coordinates persistence actions.
- **Persistence Layer**  
Responsible for data storage and retrieval. It provides repositories/DAOs (or equivalent) that the Business Logic layer uses for CRUD operations.
### Facade Pattern Explanation
The Facade Pattern streamlines interactions between layers by providing a single, simplified interface:
- The Presentation Layer calls HBnBFacade.
- The Facade coordinates business workflows (e.g., validate input, apply rules, call repositories).
- The Persistence Layer remains encapsulated behind the Facade and repository access, preventing direct coupling.

- ## Business Logic Layer

### Class Diagram

<img width="1529" height="929" alt="Class digram" src="https://github.com/user-attachments/assets/f4e2068d-cda5-463b-8f0d-3972fa3bc03c" />

#### Overview

The core entities of the system include User, Place, Review, and Amenity. Each entity:

- Has a unique identifier (ID).

- Records creation and update timestamps (for audit and tracking).

- **The relationships reflect the requirements:**

- A User can create multiple Places (ownership).

- A Place can have multiple Amenities.

- A Review references exactly one User and one Place.

#### Entities and Requirements Mapping

## User

- **Attributes (minimum required):**

- first_name

- last_name

- email

- password

- is  admin

- **Required behaviors:**

- Users can be created (registered), updated, and deleted.

## Place

- **Attributes (minimum required):**

- name

- description

- Price per night

- latitude

- longitude

- owner

- review

- amenities (list/collection of amenities)

- **Required behaviors:**

- Places can be created, updated, deleted, and listed.

## Review

- **Attributes (minimum required):**

- rating

- comment

- user (association to User)

- place (association to Place)

- **Required behaviors:**

- Reviews can be created, updated, deleted, and listed by place.

## Amenity

- **Attributes (minimum required):**

- name

- place

- **Required behaviors:**

- Amenities can be created, updated, deleted, and listed.

## API Interaction Flow

### Sequence Diagrams Overview

The sequence diagrams provide a detailed view of how core API calls are handled within the HBnB application.
They illustrate the step-by-step interaction between the Presentation Layer, Business Logic Layer, and
Persistence Layer for key user actions such as user registration, place creation, review submission,
and fetching a list of places.

These diagrams help clarify the system’s runtime behavior by showing how requests flow through the
application layers, how data is validated, and how responses are returned to the user.
They also reinforce the separation of concerns and ensure a clear understanding of system interactions
before implementation.

---

### User Registration Sequence Diagram

![User Registration Sequence Diagram](user%20registration%20diagrams%201.0.png)

This diagram illustrates the process of registering a new user, starting from the UI request and
ending with data persistence in the database.

---

### Place Creation Sequence Diagram

![Place Creation Sequence Diagram](place%20creation%20diagrams%201.0.png)

This diagram shows how a user creates a new place listing and how the request flows through the API
and Business Logic layers before being stored.

---

### Review Submission Sequence Diagram

![Review Submission Sequence Diagram](review%20submission%20diagrams%201.0.png)

This diagram represents the submission of a user review, including validation and storage.

---

### Fetching a List of Places Sequence Diagram

![Fetching a List of Places Sequence Diagram](fetching%20a%20list%20of%20places%20diagrams%201.0.png)

This diagram illustrates how the system processes a request to retrieve a list of places based on
filtering criteria.

## Conclusion
This technical documentation provides a clear and structured blueprint for HBnB Application by presenting:
- A high-level architecture with a layered design and a facade-based interaction model.
- The business entities (User, Place, Review, Amenity) and how they map to functional requirements.
- API interaction flows that demonstrate the separation of concerns across layers.

This ensures the next implementation phases can proceed with a shared understanding of the intended design and system responsibilities.

