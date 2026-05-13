from fastapi import FastAPI
from agent import run_agent

app = FastAPI()


@app.get("/")
def home():
    return {"message": "AI Agent is running"}


@app.post("/run")
def run(input_text: str):
    result = run_agent(input_text)
    return result