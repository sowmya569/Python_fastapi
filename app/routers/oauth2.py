from jose import JWTError,jwt
from datetime import datetime ,timedelta
from .. import schemas,model
from ..database import create_db_and_tables,SessionDep,Session,get_session
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException,status
from ..config import settings

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_token(data:dict):
    to_encode=data.copy()
    to_encode["user_id"] = str(data["user_id"])     
    expires=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"expires":expires.isoformat()})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    print("This isencoded_jwt", encoded_jwt)
    return encoded_jwt

def verify_access_token(token: str, credential_expection):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Decoded Payload:", payload)  # Debugging step
        user_id = payload.get("user_id")
        print("Extracted user_id from token:", user_id)  # Debugging step
        if user_id is None:
            raise credential_expection
        token_data = schemas.TokenData(id=str(user_id))  # Ensure id is a string
        print("This is the token data",token_data)
    except JWTError as e:
        print("JWT Error:", e)
        raise credential_expection
    return token_data
    
def get_user_token(session: SessionDep, token: str = Depends(oauth2_scheme)):
    credential_expection = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, credential_expection)
    print("Token Data ID:", token_data.id)  # Debugging step

    user = session.query(model.User).filter(model.User.id == int(token_data.id)).first()
    print("SQLAlchemy Query Result:", user)  # Debugging step

    if user is None:
        print("User not found!")
        raise credential_expection

    print("User found:", user)
    print("USer id is ",user.id)
    return user

