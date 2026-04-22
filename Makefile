

dev:
	uvicorn main:app --reload


check:
	uv run mypy .