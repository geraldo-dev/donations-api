from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from fastapi import Depends
from app.schemas.user import UserCreate, Login
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.utils import hash_password, hash_verify_password
from fastapi import HTTPException
from datetime import datetime, timedelta
import os

from fastapi.security import OAuth2PasswordBearer

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/user/login')


# loads the environment variables
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITM = os.getenv('ALGORITM')


class UserCase:
    def __init__(self, db_session: Session):
        self.__db_session = db_session

    def created_user(self, user: UserCreate):

        __user_model = User(
            username=user.username,
            email=user.email,
            password=hash_password(user.password)
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

    def login_user(self, username: str, password: str, expires_in: int = 30):
        __find_user = self.__db_session.query(User).where(
            User.username == username).first()

        if __find_user is None:
            raise HTTPException(
                status_code=401, detail='Invalid email or password'
            )

        if not hash_verify_password(str(password), str(__find_user.password)):
            raise HTTPException(
                status_code=401, detail='Invalid username or password'
            )

        exp = datetime.utcnow() + timedelta(minutes=expires_in)

        payload = {
            'sub': __find_user.username,
            'exp': exp
        }

        access_token = jwt.encode(payload, str(
            SECRET_KEY), algorithm=str(ALGORITM))

        # response delivery model otherwise the header does not find the token
        return {
            'access_token': access_token,
            'exp': exp.isoformat()
        }

    def token_verifier(self, access_token):
        try:
            data = jwt.decode(access_token, str(SECRET_KEY),
                              algorithms=[str(ALGORITM)])

            user_on_db = self.__db_session.query(
                User).filter_by(username=data['sub']).first()

            if user_on_db is None:
                raise HTTPException(
                    status_code=401,
                    detail='Invalid access token'
                )

        except JWTError:
            raise HTTPException(
                status_code=401,
                detail='Invalid access token'
            )

    def verifier_admin(self, access_token):
        try:
            data = jwt.decode(access_token, str(SECRET_KEY),
                              algorithms=[str(ALGORITM)])

            user_on_db = self.__db_session.query(
                User).filter_by(username=data['sub']).first()

            if user_on_db is None:
                raise HTTPException(
                    status_code=401,
                    detail='Invalid access token'
                )
            user_login: dict = user_on_db.__dict__

            if user_login['is_admin'] != True:
                raise HTTPException(
                    status_code=401,
                    detail='you are not admin'
                )

        except JWTError:
            raise HTTPException(
                status_code=401,
                detail='Invalid access token'
            )
