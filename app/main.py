from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.presentation.routes.auth_routes import authRouter
from app.presentation.routes.property_routes import propertyRouter
from app.presentation.routes.user_routes import userRouter

app = FastAPI(debug=True)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(userRouter, prefix="/api", tags=["users"])
app.include_router(propertyRouter, prefix="/api", tags=["properties"])
app.include_router(authRouter, prefix="/api", tags=["Auth"])
