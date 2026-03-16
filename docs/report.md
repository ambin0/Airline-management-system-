# Airline Management System – Project Report

## 1. Introduction

The purpose of this project is to develop a basic Airline Management System using Python. The system is intended to manage records related to clients, airlines, and flights in a structured and organised way. By separating the system into different modules and components, the program can be developed collaboratively while maintaining clear responsibilities for each team member.

The project also aims to demonstrate the use of version control through GitHub. Each member of the team works on a separate branch which allows development to take place simultaneously without interfering with the work of others. This approach reflects common practices used in professional software development environments.

## 2. Project Objectives

The main objective of the project is to design and implement a simple management system capable of storing and managing airline-related information. The system should allow records to be created, viewed, updated, and removed where necessary.

More specifically, the project aims to:

- Implement CRUD (Create, Read, Update, Delete) operations for system records.
- Store and retrieve data using JSON files.
- Organise the code using a modular structure.
- Provide a basic graphical interface to interact with the system.
- Use GitHub to manage collaboration and version control.

These objectives ensure that the system demonstrates both programming concepts and collaborative development practices.

## 3. System Overview

The Airline Management System focuses on managing three main types of records: clients, airlines, and flights.

Client records contain information relating to individuals who may use the airline service. This may include identifiers or other basic details required to manage bookings or interactions with the system.

Airline records store information about different airline companies. This allows the system to associate flights with specific airlines and maintain structured data about available services.

Flight records contain information such as the flight number, airline, departure location, destination, and other relevant details. These records represent the core operational information managed by the system.

All records are stored using JSON files. This format was chosen because it is lightweight, easy to read, and well supported within Python. It allows data to be stored persistently while remaining simple to manage within the project.

## System Architecture

```

                 +----------------------+
                 |        GUI           |
                 |  User Interface     |
                 | (src/gui)           |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 |      CRUD Layer      |
                 | Create / Read /      |
                 | Update / Delete      |
                 | (record operations)  |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 |    Validation Layer  |
                 | Data integrity       |
                 | Format checks        |
                 | Duplicate prevention |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 |     Storage Layer    |
                 | Load & Save Records  |
                 | JSONL File Handling  |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 |     Data Storage     |
                 |     record.jsonl     |
                 | Persistent Records   |
                 +----------------------+
```
## 4. System Structure

To maintain organisation and clarity within the codebase, the project is divided into several directories, each serving a specific purpose.

The `modules` directory contains the core logic for managing clients, airlines, flights, and data storage. Separating this logic into individual modules makes the program easier to maintain and extend.

The `data` directory contains JSON files used to store system data. These files allow the program to load and save records as needed.

The `gui` directory contains the user interface components that allow users to interact with the system in a more accessible way.

The `tests` directory contains unit tests which are intended to verify that individual parts of the program behave as expected.

Finally, the `docs` directory contains documentation related to the project, including this report and any meeting notes produced during development.

This structure allows the project to remain organised while different team members work on separate areas of the system.

## 5. Development Workflow

The project is managed using GitHub as the primary version control platform. A branching strategy is used in order to separate different areas of development.

Each team member is assigned a branch corresponding to their role within the project. For example, branches are used for the graphical interface, CRUD functionality, data storage, flight logic, testing, and documentation.

By working on separate branches, team members can develop their components independently. Changes can later be reviewed and merged into the main branch once they are stable and complete.

This workflow reduces the likelihood of conflicts while also encouraging a more organised development process.

## 6. Conclusion

The Airline Management System project demonstrates the process of designing and implementing a structured software system using Python. By dividing the project into multiple components and assigning clear roles to each team member, the development process becomes more manageable and collaborative.

The use of GitHub for version control allows the team to coordinate development while maintaining a clear record of changes. In addition, the modular design of the system helps ensure that different parts of the program can be developed, tested, and maintained independently.

Overall, the project provides practical experience in both programming and collaborative software development.
