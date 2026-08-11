from fastapi import FastAPI
from .database import engine
from . import models
from .routers import post, user, auth,votes
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# CORS origins - define allowed origins for cross-origin requests
origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

models.Base.metadata.create_all(bind=engine)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)


