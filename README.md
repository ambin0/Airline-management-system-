# Record Management System

This repository holds our group project for the Record Management System assignment. We're building a tool for a specialist travel agent to manage their client, airline, and flight records.

### What it Does

The main goal of this application is to provide a simple interface for the travel agent to perform the following actions:

* **Create**, **delete**, and **update** records for clients, airlines, and flights.
* **Search for** and **display** specific records.

All the data is stored locally in a `record.jsonl` file, so the information is saved even after the application is closed.

### Project Structure

Here's a quick look at how the project is organized:

```text
docs/
README.md
requirements.txt
src/
  conf/
  data/
  gui/
  main.py
  record/
    record.jsonl
tests/
```

### Our Team

* **Member 1:** GUI / UX
* **Member 2: Abdel Fattah Hasan:** CRUD logic
* **Member 3:** Storage and integration
* **Member 4:** Validation / flight logic support
* **Member 5:** Testing
* **Member 6:** Project management and documentation

### My Contribution (Abdel Fattah Hasan)

As Member 2, I was responsible for the core CRUD (Create, Read, Update, Delete) logic for:

* Client records
* Airline records
* Flight records

I've created the following files:

* `src/record/crud\_helpers.py`
* `src/record/client\_crud.py`
* `src/record/airline\_crud.py`
* `src/record/flight\_crud.py`

And the corresponding test files:

* `tests/test\_crud\_helpers.py`
* `tests/test\_client\_crud.py`
* `tests/test\_airline\_crud.py`
* `tests/test\_flight\_crud.py`

### A Few Notes for the Team

#### For Member 1 (GUI)

Feel free to call the CRUD functions directly from the GUI. Just make sure to use the shared `records` list that's already loaded in memory. Please avoid putting any file loading or saving logic in the GUI code.

#### For Member 3 (Storage)

Let's keep the storage logic separate from the CRUD operations. The CRUD functions are designed to work with the `records: list\[dict]` in memory. Your part of the code should handle loading the records from `src/record/record.jsonl` when the app starts and saving them when it closes.

#### For Members 4 \& 5 (Validation / Testing)

Just a heads-up: flight records don't have a unique ID in the project brief. To match a flight record, you'll need to use a combination of:

* `Client\_ID`
* `Airline\_ID`
* `Date`
* `Start City`
* `End City`

#### How to Run the Project

1. Install the necessary packages: `pip install -r requirements.txt`
2. Run the main application: `python src/main.py`
3. The GUI should pop up, and you can start managing the records.

### Running the Tests

To run the unit tests, just run this command from the project's root directory:

```bash
python -m unittest discover -s tests -v
```

#### Git Branches

We're using the following branches for our work:

* `gui`
* `crud`
* `storage`
* `flight\_logic`
* `testing`
* `documentation`

#### Commit Style

Let's try to keep our commits focused on a single logical change. For example:

* `crud: Add shared record helper functions.`
* `crud: Implement client CRUD functions.`
* `tests: Add flight CRUD unit tests.`

## Final Note

Let's make sure we all merge our work into the main branch before the final submission.

