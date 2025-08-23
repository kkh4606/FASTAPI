from fastapi import status, Depends, HTTPException, Response, APIRouter
from .. import models, database, schemas, oauth2

from sqlalchemy.orm import Session
from typing import List, Optional


router = APIRouter(tags=["VOTE"])


@router.post("/vote", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    current_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db),
):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id : {vote.post_id} does not exist",
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user.id,
    )

    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"already voted with id : {current_user.id} on post : {vote.post_id}",
            )

        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "succesfully vote"}

    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote does not exit",
            )

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}
