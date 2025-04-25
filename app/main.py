from fastapi import FastAPI
from app.api.routes import ocr

app = FastAPI(title="OCR API", version="1.0", redirect_slashes=False)

# Include OCR routes
app.include_router(ocr.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Welcome to the OCR API!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8003, log_level="debug")
