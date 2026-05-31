from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth
from app.routes.emotion_mediapipe import router as emotion_router
from app.routes.age_mediapipe import router as age_router

app = FastAPI(title="Emotion & Age Detection API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(emotion_router, prefix="/api/detect", tags=["Emotion Detection"])
app.include_router(age_router, prefix="/api/detect", tags=["Age Detection"])

@app.get("/")
async def root():
    return {"message": "Emotion & Age Detection API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}