from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models import *
from authentication import (get_hash_password)
app = FastAPI()

@app.post("/registration")
async def user_registration(user: user_pydantic_in):
    user_info = user.dict(exclude_unset=True)
    user_info["password"] = get_hash_password(user_info["password"])
    user_obj = await User.create(**user_info)
    new_user = await user_pydantic.from_tortoise_orm(user_obj)
    return{
        "status": "ok",
        "data": f"Hello {new_user.username}, thanks for choosing our services. Please check 
        your email inbox and click on the link to confirm your registra tion"
    }


@app.get("/")
def index():
    return {"Message": "Hello World"}



register_tortoise(
    app,
    db_url="sqlite://database.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)