import os
import random
from datetime import datetime, timedelta
from typing import Optional

from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_otp(plain_otp: str, hashed_otp: str) -> bool:
    return pwd_context.verify(plain_otp, hashed_otp)

def get_otp_hash(otp: str) -> str:
    return pwd_context.hash(otp)


def create_otp() -> str:
    return str(random.randint(100000, 999999))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def send_otp_email(email: str, otp: str):
    """
    Mock function to "send" an email.
    In a real application, this would use a service like SendGrid or SMTP.
    """
    print("--- MOCK EMAIL SERVICE ---")
    print(f"To: {email}")
    print(f"Subject: Your OTP Code")
    print(f"Your OTP code is: {otp}")
    print("--------------------------")