from tortoise import Tortoise
import os

async def init_database():
    await Tortoise.init(
        db_url=os.getenv("DATABASE_URL"),
        modules={'models':['models.user_model']}
    )
    await Tortoise.generate_schemas()