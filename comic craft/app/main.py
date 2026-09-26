import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router

# Ensure runtime static directories exist
os.makedirs(os.path.join("static", "panels"), exist_ok=True)
os.makedirs(os.path.join("static", "exports"), exist_ok=True)
os.makedirs(os.path.join("static", "css"), exist_ok=True)
os.makedirs(os.path.join("static", "images"), exist_ok=True)

app = FastAPI(
    title="ComicCraft - AI Comic Story Creator",
    description="Create personalized AI comic stories and illustrations with Google Gemini & Stable Diffusion",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
