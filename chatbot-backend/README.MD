pip install -r requirements.txt

source venv/bin/activate

uvicorn main:app --reload --port 8080
