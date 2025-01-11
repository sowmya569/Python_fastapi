from .. import model,schemas,utils
from fastapi import Body, FastAPI, HTTPException, Query, Response,status,APIRouter
from ..database import create_db_and_tables,SessionDep

router=APIRouter(
    prefix="/users",
    tags=['User']
)

@router.post('/',response_model=schemas.UserOut)
def create_user(data:schemas.UserCreate,response:Response,session:SessionDep):
    response.status_code=status.HTTP_201_CREATED
    # instead of having this in one file we can seperate the file and keep the hash file in different file
    hashed_password=utils.hash(data.password)
    data.password=hashed_password
    new_user=model.User(**data.dict())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.get("/all", status_code=status.HTTP_200_OK)
def get_all_user(session: SessionDep):
    user = session.query(model.User).all()
    print(user)
    return user

@router.get("/{id}",response_model=schemas.UserOut,status_code=status.HTTP_200_OK)
def get_user(id:int,response:Response,session:SessionDep):
    user=session.query(model.User).filter(model.User.id==id).first()
    print(user)
    if not user:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {f"{id} details are ":"Not found"}
    return user
