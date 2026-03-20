from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Coding Mentor API is running "}