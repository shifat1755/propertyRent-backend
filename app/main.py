from fastapi import FastAPI

from app.presentation.routes.user_routes import userRouter

app = FastAPI(debug=True)


app.include_router(userRouter, prefix="/api", tags=["users"])
