from fastapi import Body, HTTPException, APIRouter
from pydantic import BaseModel
from models.Admin import Admin
from crud.admin_crud import add_admin
from auth.jwt_handler import sign_jwt

from passlib.context import CryptContext

router = APIRouter()

hash_helper = CryptContext(schemes=['bcrypt'])


class AdminLogin(BaseModel):
    email: str
    password: str


@router.post("/login")
async def admin_login(admin_credentials: Admin = Body()):
    admin_doc = await Admin.find_one(Admin.email == admin_credentials.email)
    if admin_doc:
        password = hash_helper.verify(
            admin_credentials.password, admin_doc.password)
        if password:
            return sign_jwt(str(admin_doc.id))

        raise HTTPException(
            status_code=403, detail='Incorrect Email or Password')

    raise HTTPException(
        status_code=403, detail='Incorrect Email or Password')
    # else:
    #     admin_credentials.password = hash_helper.hash(
    #         admin_credentials.password)
    #     admin = await add_admin(admin_credentials)
    #     return sign_jwt(str(admin.id))

    # raise HTTPException(
    #     status_code=403, detail='Incorrect Email or Password')
