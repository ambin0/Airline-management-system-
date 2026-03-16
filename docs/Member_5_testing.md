## Member 5 – Testing

### Goal
Ensure the system works correctly through **unit and integration testing**.

### Responsibilities
- Unit tests for all modules  
- Integration tests for full workflow  
- Identify bugs and edge cases  

### Files
tests/test_client_crud.py
tests/test_airline_crud.py
tests/test_flight_crud.py
tests/test_storage.py
tests/test_validation.py
tests/test_integration.py
### How It Should Work
- Unit tests verify individual modules  
- Integration tests verify system lifecycle:
  - load records  
  - modify records  
  - save records  
  - restart application  

### Task List
1. Review modules to determine required tests  
2. Implement unit tests  
3. Implement integration tests  
4. Identify and report bugs  

### Things to Watch Out For
- Edge cases in records  
- Invalid inputs  
- Storage or validation failures  
- Test stability as code evolves  
