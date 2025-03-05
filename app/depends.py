from sqlalchemy.orm import Session
from fastapi import Depends
from app.auth import UserCase
from fastapi.security import OAuth2PasswordBearer
from app.config import SessionLocal

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/user/login')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def token_verifier(
    db_session: Session = Depends(get_db),
    token=Depends(oauth_scheme)
):
    uc = UserCase(db_session)
    uc.token_verifier(access_token=token)
