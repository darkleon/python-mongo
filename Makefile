run-prod:
	uvicorn main:app --port 8081 --reload

run:
	fastapi run main.py --port 8081 --reload

install:
	pip install -r requirements.txt