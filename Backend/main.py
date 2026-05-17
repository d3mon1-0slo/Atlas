from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import generate
from api import projects
from api import scrape

import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins =["*"],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers=["*"],
)


app.include_router(generate.router, prefix="/api/v1", tags=["api"])


