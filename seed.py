from app.models.user import User
from app.utils import hash_password
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


# loads the environment variables
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(str(DATABASE_URL), pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()


def user_admin(username: str, email: str, password: str):
    """Cria um usuário admin se ele não existir"""

    __user_model = User(
        username=username,
        email=email,
        is_admin=True,
        password=hash_password(password)
    )

    try:

        existing_admin = db.query(
            User).filter(User.email == __user_model.email).first()
        if not existing_admin:

            db.add(__user_model)
            db.commit()
            db.refresh(__user_model)
            print("Usuário admin criado com sucesso!")
        else:
            print("Usuário admin já existe.")
    except:
        print('ops.....')


if __name__ == '__main__':
    user_admin(
        username='admin2',
        email='admin2@example.com',
        password='admin123'
    )
