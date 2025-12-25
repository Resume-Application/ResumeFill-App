import os
from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth, OAuthError

load_dotenv()
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}