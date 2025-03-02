from app.schemas.user import UserCreate
from app.depends import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.auth import UserCase
# from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix='/user')


@router.post('/register', status_code=201)
def user_register(user: UserCreate, db_session: Session = Depends(get_db)):
    new_user = UserCase(user, db_session)
    new_user.check_by_email()

    return new_user.created_user()
