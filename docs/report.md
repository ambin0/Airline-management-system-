# Airline Management System – Project Report

## 1. Introduction
The Airline Management System is a Python-based software project designed to manage airline-related data including clients, airlines, and flights. The goal of the system is to provide a structured way to store, retrieve, and manage information using modular programming and version control through GitHub.

This project is developed collaboratively by a team, with each member responsible for a different component of the system such as the graphical user interface, data storage, core program logic, testing, and documentation.

## 2. Project Objectives
The main objectives of this project are:

- To design a structured Python program using multiple modules
- To implement CRUD (Create, Read, Update, Delete) functionality for system records
- To store and retrieve data using JSON files
- To develop a simple graphical user interface
- To collaborate using GitHub branches and version control

## 3. System Overview
The system manages three main types of records:

### Clients
Client records store information about customers who may book flights. This can include details such as the client name, ID, and contact information.

### Airlines
Airline records contain information about different airline companies operating flights.

### Flights
Flight records include information such as flight number, airline, departure location, destination, and time.

These records are stored using JSON files to allow easy saving and loading of data.

## 4. System Architecture
The system is structured into multiple folders and modules to keep the code organized.

- `modules/` contains the main logic for clients, airlines, and flights
- `data/` stores JSON files used to save system data
- `gui/` contains the graphical user interface
- `tests/` contains unit tests for validating program functionality
- `docs/` contains documentation and the project report

This modular structure allows different team members to work on separate components of the system simultaneously.

## 5. Development Workflow
The team uses GitHub to manage the project and collaborate effectively. Each member works on a separate Git branch based on their assigned role. This prevents conflicts and allows work to be developed independently.

Branches used in the project include:

- `gui` – User interface development
- `crud` – Core data management functions
- `storage` – JSON data handling
- `flight_logic` – Flight validation and system logic
- `testing` – Unit testing
- `documentation` – Project documentation and reporting

Changes are merged into the main branch once they are completed and reviewed.

## 6. Conclusion
The Airline Management System project demonstrates the use of modular programming, version control, and collaborative development practices. By separating the system into different components and using GitHub branches, the team can work efficiently while maintaining an organized codebase.
