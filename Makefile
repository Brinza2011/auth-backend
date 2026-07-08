

dev:
	uv run uvicorn main:app --reload


check:
	uv run mypy .


ci: 
	uv run ruff check
	uv run ruff format ./file.py
