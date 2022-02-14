from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from db.session import get_db
from sqlalchemy.orm import Session
from core.hashing import Hasher
from db.repository.users import get_user_by_username
from core.security import decode_jwt_access_token, encode_jwt_access_token

router = APIRouter()

credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Couldn't validate credentials")


@router.post('/')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    username = request.username
    password = request.password
    user = get_user_by_username(username=username, db=db)
    if not user:
        raise credentials_exception
    if not Hasher.verify_password(password, user.hashed_password):
        raise credentials_exception
    return {
        "access_token": encode_jwt_access_token(data={
            "username": user.username,
            "user_id": user.id
        }),
        "token_type": "bearer"
    }


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user_from_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        username = decode_jwt_access_token(token).get("username")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(username=username, db=db)
    if user is None:
        raise credentials_exception
    return user
