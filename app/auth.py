from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import HTTPException
from datetime import datetime, timedelta
import os

# loads the environment variables
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITM = os.getenv('ALGORITM')

# gerado de senha com hash
crypt_context = CryptContext(schemes=['sha256_crypt'])


class UserCase:
    def __init__(self, db_session: Session):
        # self.__username = user.username
        # self.__email = user.email
        # self.__password = user.password
        self.__db_session = db_session

    def created_user(self, user: UserCreate):

        # def created_user(self):
        __user_model = User(
            username=user.username,
            email=user.email,
            password=crypt_context.hash(user.password)
        )

        try:

            self.__db_session.add(__user_model)
            self.__db_session.commit()
            self.__db_session.refresh(__user_model)
            return f'{user.username}'
        except IntegrityError:

            raise HTTPException(
                status_code=401, detail='Invalid username or password')

    def check_by_email(self, email: str):
        user = self.__db_session.query(User).where(
            User.email == email).first()

        if user:
            raise HTTPException(
                status_code=400, detail='email already exists')
        return False

    def get_by_id(self, user_id: int):
        user = self.__db_session.query(User).where(
            User.user_id == user_id).first()

        if not user:
            raise HTTPException(
                status_code=404, detail='user not found')
        return user
