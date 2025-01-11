from fastapi import APIRouter, Body, FastAPI, HTTPException, Query, Response,Depends,status
from .oauth2 import get_user_token
from .. import model,schemas,utils
from ..database import create_db_and_tables,SessionDep,Session, get_session

router=APIRouter(prefix="/vote",tags=['VOTE']) 

@router.post('/',status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,session:SessionDep,current_user:int=Depends(get_user_token)):
    vote_query=session.query(model.Vote).filter(model.Vote.post_id==vote.post_id,model.User.id==current_user.id)
    if not vote_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post not found")
    valid_vote=vote_query.first()
    # print(model.Post)
    if(vote.dir==1):
        if valid_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
        detail=f"{current_user.id} as already like the post {vote.post_id}")
        new_vote=model.Vote(post_id=vote.post_id,user_id=current_user.id)
        session.add(new_vote)
        session.commit()
        return{"Vote added":"Successfully"}
    else:
        # Basically deleting the preexisting vote
        if not valid_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Vote does not exist")
        session.delete(valid_vote)
        session.commit()
        return{"Successfully":"Data is deleted"}
    