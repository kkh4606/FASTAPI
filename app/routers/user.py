from fastapi import status, Depends, HTTPException, Response, APIRouter
from .. import models, database, schemas, utils, oauth2

from sqlalchemy.orm import Session
from typing import List


router = APIRouter(prefix="/users", tags=["USERS"])


@router.get("/", response_model=List[schemas.UserOut])
def get_users(
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    users = db.query(models.User).all()
    return users


# @router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
@router.post(
    "/register", response_model=schemas.UserRegOut, status_code=status.HTTP_201_CREATED
)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):

    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = oauth2.create_access_token(data={"user_id": new_user.id})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_details": new_user,
    }


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id : {id} not found",
        )

    return user


@router.put("/{id}", response_model=schemas.UserOut)
def update_user(
    id: int, user_update: schemas.UserUpdate, db: Session = Depends(database.get_db)
):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    if user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id : {id} not found",
        )

    user_query.update(user_update.model_dump(), synchronize_session=False)
    db.commit()

    return user


@router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(database.get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)

    if user_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id : {id} was not found",
        )

    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
