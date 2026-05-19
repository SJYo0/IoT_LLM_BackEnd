#-----[ FastAPI ]-----------------------
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from AiAnalysis.routers import AiAnalysis

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(AiAnalysis.router)
