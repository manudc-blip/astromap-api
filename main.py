from fastapi import FastAPI

app = FastAPI(title="AstroMap API")

@app.get("/")
def root():
    return {"message": "AstroMap API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}