from fastapi import FastAPI

app = FastAPI()


@app.post("/api/1/import")
async def root():
    return {"message": "Hello World"}
