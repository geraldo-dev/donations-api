# from sqlalchemy.orm import Session
# from fastapi import Depends
# from app.auth import Toke
from fastapi.security import OAuth2PasswordBearer
from app.config import SessionLocal

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/user/login')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
