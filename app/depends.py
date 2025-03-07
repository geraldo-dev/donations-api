from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.auth import UserCase
from app.config import SessionLocal
from fastapi import Depends

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


def token_verifier_admin(
    db_session: Session = Depends(get_db),
    token=Depends(oauth_scheme)
):
    uc = UserCase(db_session)
    uc.verifier_admin(access_token=token)
