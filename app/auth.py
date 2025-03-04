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
    def __init__(self, user: UserCreate, db_session: Session):
        self.__username = user.username
        self.__email = user.email
        self.__password = user.password
        self.__db_session = db_session

    def created_user(self):
        __user_model = User(
            username=self.__username,
            email=self.__email,
            password=crypt_context.hash(self.__password)
        )

        try:

            self.__db_session.add(__user_model)
            self.__db_session.commit()
            self.__db_session.refresh(__user_model)
            return f'{self.__username}'
        except IntegrityError:

            raise HTTPException(
                status_code=401, detail='Invalid username or password')

    def check_by_email(self):
        user = self.__db_session.query(User).where(
            User.email == self.__email).first()

        if user:
            raise HTTPException(
                status_code=400, detail='email already exists')
        return False
