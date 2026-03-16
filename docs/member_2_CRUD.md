## Member 2 – CRUD Logic (Abdel Fattah Hasan)

### Goal
Implement the **core business logic** for creating, reading, updating, and deleting records. CRUD functions operate on the in-memory `list[dict]` record structure.

### Responsibilities
- CRUD for clients, airlines, and flights  
- Reusable helper functions  
- Consistent record handling  
- Unit tests for CRUD functionality  

### Files
src/record/crud_helpers.py
src/record/client_crud.py
src/record/airline_crud.py
src/record/flight_crud.py
tests/test_crud_helpers.py
tests/test_client_crud.py
tests/test_airline_crud.py
tests/test_flight_crud.py

### How It Should Work
- Operates on `records: list[dict]`  
- Called by GUI to perform operations  
- Prevents duplicate entries and ensures consistent formatting  

### Task List
1. Implement helper functions  
2. CRUD logic for client records  
3. CRUD logic for airline records  
4. CRUD logic for flight records  
5. Write unit tests  

### Things to Watch Out For
- Maintaining consistent record formats  
- Preventing duplicates  
- Handling invalid input safely  
