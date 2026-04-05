# High-Level Package Diagram for HBnB Application

## Overview
This document provides a high-level architecture diagram illustrating the three-layer structure of the HBnB application and how the layers interact using the Facade Pattern. The goal is to provide a clear conceptual overview of how the system is organized before implementation.


## Three-Layer Architecture
The application is structured into three primary layers:

### Presentation Layer (Services, API)
-	Responsible for handling user interactions (API endpoints).
-	Validates and parses requests, then forwards them to a single-entry point (Facade).
-	Doesn’t directly access persistence/database logic.
  
### Business Logic Layer (Core Logic, Models)
-	Contains the application’s core rules and workflows.
-	Defines domain entities (e.g., User, Place, Review, Amenity).
-	Provides HBnBFacade that exposes a simplified interface to the Presentation Layer.
  
### Persistence Layer (Database Access)
-	Responsible for storing and retrieving data.

## HBNB Package Diagram:
<img width="1723" height="1416" alt="HBNB PackageDiagram" src="https://github.com/user-attachments/assets/850ded9d-2c80-45a3-9c05-0a03484c02a6" />



## Facade Pattern Explanation
The Facade Pattern streamlines interactions between layers by providing a single, simplified interface:
-	The Presentation Layer calls HBnBFacade.
-	The Facade coordinates business workflows (e.g., validate input, apply rules, call repositories).
-	The Persistence Layer remains encapsulated behind the Facade and repository access, preventing direct coupling.


## Conclusion
This document provides a clear high-level blueprint for HBnB’s architecture. The Facade Pattern ensures the Presentation Layer communicates with the rest of the system through a single gateway, avoiding direct dependencies between layers and keeping the architecture clean and scalable.
