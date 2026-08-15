import os
from dotenv import load_dotenv
from datetime import datetime , timedelta , timezone
from jose import jwt , JWTError
from fastapi.security import OAuth2PasswordBearer 
from fastapi import Depends , HTTPException  , status
from sqlalchemy.orm import Session
from database import get_db
import models



load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"wwww.Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],

        )
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception


    except JWTError:
        raise credentials_exception

    user = (
        db.query(models.User).filter(models.User.id==int(user_id))
        .first()

    )

    if user is None:
        raise credentials_exception



    return user




def create_access_token(data:dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    