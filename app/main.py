from fastapi import FastAPI

from app.presentation.routes.property_routes import propertyRouter
from app.presentation.routes.user_routes import userRouter

app = FastAPI(debug=True)


app.include_router(userRouter, prefix="/api", tags=["users"])
app.include_router(propertyRouter, prefix="/api", tags=["properties"])
