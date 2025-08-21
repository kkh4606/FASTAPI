from fastapi import status, Depends, HTTPException, Response, APIRouter
from .. import models, database, oauth2, schemas, utils
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from typing import List


router = APIRouter(tags=["AUTHENTICATION"])


@router.post("/login", response_model=schemas.Token)
def login_user(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):

    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials"
        )

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials"
        )

    # create_token

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    tokenData = schemas.Token(access_tokne=access_token, token_type="bearer")

    return tokenData
