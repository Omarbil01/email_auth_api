from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, models, schemas, security
from .database import get_db

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user with an email address.
    - Validates email format and checks for duplicates.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    crud.create_user(db=db, user=user)
    return {"message": "Registration successful. Please request an OTP to login."}


@router.post("/request-otp")
def request_otp(otp_request: schemas.OTPRequest, db: Session = Depends(get_db)):
    """
    Generate and send an OTP to the user's registered email.
    """
    user = crud.get_user_by_email(db, email=otp_request.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    otp = security.create_otp()
    crud.store_otp(db, email=user.email, otp=otp)


    security.send_otp_email(user.email, otp)

    return {"message": "OTP sent to your email."}


@router.post("/verify-otp", response_model=schemas.Token)
def verify_otp(otp_verify: schemas.OTPVerify, db: Session = Depends(get_db)):
    """
    Verify the OTP and log the user in by providing a JWT token.
    """
    user = crud.get_user_by_email(db, email=otp_verify.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not registered.",
        )

    if not user.hashed_otp or not user.otp_expiry:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP not requested. Please request an OTP first.",
        )

    if datetime.utcnow() > user.otp_expiry:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP has expired. Please request a new one.",
        )

    if not security.verify_otp(otp_verify.otp, user.hashed_otp):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP.",
        )


    user.hashed_otp = None
    user.otp_expiry = None
    db.commit()


    access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}