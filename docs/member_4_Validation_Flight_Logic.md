## Member 4 – Validation & Flight Logic

### Goal
Ensure **data integrity** by validating records, preventing duplicates, and enforcing correct formats, especially for flight records.

### Responsibilities
- Implement flight validation rules  
- Verify required fields  
- Check relationships between clients and airlines  
- Prevent duplicate flight entries  

### Files
src/record/validation.py
src/record/flight_crud.py (updates)
tests/test_validation.py
tests/test_flight_crud.py
### How It Should Work
- Validate flights before creation or update  
- Ensure required fields are present  
- Ensure referenced client and airline exist  
- Prevent duplicates using composite key:
  Client_ID + Airline_ID + Date + Start City + End City

### Task List
1. Implement validation functions  
2. Integrate validation into flight CRUD  
3. Ensure proper error handling  
4. Write tests  

### Things to Watch Out For
- Invalid date formats  
- Missing required fields  
- References to non-existent records  
- Duplicate flight entries  
