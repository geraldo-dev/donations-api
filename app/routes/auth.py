from app.schemas.user import UserCreate, UserResponse
from app.depends import get_db, token_verifier, token_verifier_admin
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.auth import UserCase
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()


@router.post('/register', status_code=201)
def user_register(user: UserCreate, db_session: Session = Depends(get_db), Auth=Depends(token_verifier_admin)):
    new_user = UserCase(db_session)
    # verifica se admin
    new_user.check_by_email(user.email)

    return new_user.created_user(user)


@router.get('/{user_id}', status_code=200, response_model=UserResponse)
def get_user(user_id: int, db_session: Session = Depends(get_db), Auth=Depends(token_verifier_admin)):

    new_user = UserCase(db_session)
    # verifica se admin
    return new_user.get_by_id(user_id)


@router.post('/login', status_code=200)
def user_login(
        user: OAuth2PasswordRequestForm = Depends(),
        db_session: Session = Depends(get_db)):
    n_user = UserCase(db_session)
    result = n_user.login_user(user.username, user.password)
    return result
