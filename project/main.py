from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from project.apps import auth, follow, like


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(follow.router)
app.include_router(like.router)


if __name__ == '__main__':
    uvicorn.run("project.main:app", host="0.0.0.0", port=8000, reload=True)
