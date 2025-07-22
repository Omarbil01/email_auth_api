from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from . import models, schemas, security

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def store_otp(db: Session, email: str, otp: str):
    user = get_user_by_email(db, email)
    if user:
        hashed_otp = security.get_otp_hash(otp)
        # OTP is valid for 5 minutes
        expiry_time = datetime.utcnow() + timedelta(minutes=5)
        user.hashed_otp = hashed_otp
        user.otp_expiry = expiry_time
        db.commit()
        db.refresh(user)
    return user