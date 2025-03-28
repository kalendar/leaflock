# leaflock
OELMs generative textbook definition.

## Current Definitions
- ✅ SQLAlchemy (`/tables`)
- ✅ Pydantic
- ⬜ . . .

## How are OELM Textbooks Stored?
Textbooks are entries within an SQLite database. A textbook can be exported/imported as a single SQLite file.

## Development
1. Clone this repo and run `uv sync --extra dev`.
2. Enter the python venv with either `.venv\Scripts\activate` on Windows, or `source .venv/bin/activate` on Unix.
3. Run `pre-commit install`.