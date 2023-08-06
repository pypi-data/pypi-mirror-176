import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from lndb_rest_instance.routers import metadata

root_path = "/" + os.getenv("ROOT_PATH", "")

app = FastAPI(openapi_prefix=root_path)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(metadata.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, root_path=root_path)
