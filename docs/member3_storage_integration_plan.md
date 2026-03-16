# My Plan for Storage & Integration (Member 3)

## Goal
My main job is to get the file saving and loading working properly. I need to make sure that when the app starts, it loads any existing records, and when it closes, it saves everything back to the file. I also need to make sure my code doesn't crash the app if the file is missing or has junk in it.

## What I'm Responsible For
- Loading records from `record.jsonl` at startup.
- Saving the records back to the file when the app closes.
- Making sure everything still works with the `list[dict]` structure that the CRUD functions use.
- Writing tests for my storage code and for the overall save/load process.

## What I'll Be Working On
- `src/data/storage.py` (this is where my main code will go)
- `tests/test_storage.py`
- `tests/test_integration.py`

## How It Should Work
1.  When the app starts, it should check for the `record.jsonl` file.
2.  If there's no file, or the file is empty, the app should just start with an empty list of records. No big deal.
3.  If the file is there and has records, load them into memory.
4.  If the file has some garbage in it (like bad JSON), the app should just ignore it and start with an empty list instead of crashing.
5.  When the user closes the app, we need to save the current list of records to the file *before* the window closes.

## My Task List

- **Standardize the file path:** I'll make a helper function to figure out where the `record.jsonl` file is, so we don't have to worry about relative paths. It should also be easy to override for testing.
- **Improve the loading logic:** Make it tougher so it can handle missing files, empty files, and bad data without crashing.
- **Improve the saving logic:** Make sure we're saving a valid list of dictionaries, and that the app only closes after the save is finished.
- **Write tests:** I'll add unit tests for all the edge cases I can think of (missing file, empty file, bad JSON, etc.) and a couple of integration tests to make sure the whole open -> change -> close -> reopen cycle works.

## A Few Things to Watch Out For
- The app crashing at startup because of a bad records file.
- The GUI closing before the records are finished saving.
- Path issues if someone runs the app from a different directory.

That's the plan. Should be pretty straightforward. I'll start with the path resolution and then move on to the loading/saving logic.
