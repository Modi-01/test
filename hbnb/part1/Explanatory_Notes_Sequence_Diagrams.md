# Explanatory Notes – Sequence Diagrams

This document provides detailed explanatory notes for the sequence diagrams created for the HBnB application as part of the API Interaction Flow documentation.

The sequence diagrams aim to:
- Illustrate how core API calls are processed within the system.
- Show interactions between the Presentation Layer (UI & API), Business Logic Layer, and Persistence Layer (Database).
- Demonstrate runtime behavior and request handling before implementation.
- Reinforce separation of concerns across system layers.

![User Registration Sequence Diagram](./user%20registration%20diagrams%201.0.png)

*User Registration Flow:*
- The user accesses the registration page through the UI.
- User details (name, email, password) are entered and submitted.
- The UI sends a registration request to the API.
- The API forwards the request to the Business Logic layer for validation.
- After successful validation, user data is stored in the database.
- A success response is returned to the user through the API and UI.

This flow highlights proper validation, secure data handling, and clear responsibility separation.

![Place Creation Sequence Diagram](./place%20creation%20diagrams%201.0.png)

*Place Creation Flow:*
- The user fills in the place creation form through the UI.
- Place data is submitted to the API.
- The API forwards the request to the Business Logic layer.
- Place information is validated and prepared for persistence.
- The place is stored in the database.
- A confirmation response is returned to the user.

This sequence demonstrates controlled data flow and correct handling of user-generated content.

![Review Submission Sequence Diagram](./review%20submission%20diagrams%201.0.png)

*Review Submission Flow:*
- The user writes a review including a rating and comment.
- Review data is submitted through the UI to the API.
- The API forwards the request to the Business Logic layer.
- Review data is validated and associated with the correct user and place.
- The review is stored in the database.
- A success response is returned to the user.

This diagram emphasizes data integrity and consistent review handling.

![Fetching a List of Places Sequence Diagram](./fetching%20a%20list%20of%20places%20diagrams%201.0.png)

*Fetching Places Flow:*
- The user requests a list of places through the UI.
- The request is sent to the API.
- The API forwards the request to the Business Logic layer.
- Filtering and sorting rules are applied.
- The database is queried for matching places.
- The resulting list is returned and displayed to the user.

This sequence highlights efficient data retrieval and smooth interaction between system layers.
