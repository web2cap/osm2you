from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI

from app.api.v1.trip import router as trip_router

app = FastAPI()

app.include_router(trip_router)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app = VersionedFastAPI(
    app,
    version_format="{major}",
    prefix_format="/v{major}",
)
