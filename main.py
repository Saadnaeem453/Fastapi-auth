from fastapi import FastAPI
from controllers import auth_controller
from helpers.init_database import init_database
app = FastAPI()


app.include_router(auth_controller.router, prefix="/api/auth")
app.add_event_handler("startup" , init_database)
@app.get("/")
async def get_api():
    return {"message": "Welcome to the API"}