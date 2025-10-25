from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router 

app = FastAPI()

# Optional: add CORS if you have a frontend on a different port
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"] if using Vite/React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)

@app.get("/")
def root():
    return {"message": "Backend running!"}
