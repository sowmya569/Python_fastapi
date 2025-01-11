from fastapi import Response,APIRouter,Depends,status,HTTPException
from ..database import SessionDep,Session, get_session
from ..schemas import UserLogin
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import model,schemas,utils
from ..routers import oauth2


router=APIRouter(tags=['Authentication'])  

@router.post('/login',response_model=schemas.Token)
# def login_user(user_credentials:OAuth2PasswordRequestForm = Depends(),session: SessionDep,response:Response):
def login_user(
    session: SessionDep,
    response: Response,
    user_credentials: OAuth2PasswordRequestForm = Depends()
):
    
    passuser=session.query(model.User).filter(model.User.email==user_credentials.username).first()
    
    if not passuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid credentials")
    
    if not utils.verify(user_credentials.password,passuser.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid credentials")
    
    access_token = oauth2.create_token(data={"user_id":passuser.id})
    return {"access_token":access_token,"token_type":"bearer"}

    