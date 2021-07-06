from fastapi import FastAPI

import uvicorn

from project.apps import auth


if __name__ == '__main__':
    app = FastAPI()

    app.include_router(auth.router)

    uvicorn.run(app, host="0.0.0.0", port=8000)
