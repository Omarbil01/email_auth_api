# OTP Authentication API

A FastAPI-based authentication system using One-Time Passwords (OTP) for secure user login.

## Features

- User registration and login with OTP verification
- JWT token-based authentication
- Rate limiting for security
- SQLAlchemy ORM with SQLite database
- Password hashing with bcrypt

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and update the values:
   ```bash
   cp .env.example .env
   ```
5. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## Environment Variables

- `SECRET_KEY`: JWT secret key (generate a secure one)
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time
- `DATABASE_URL`: Database connection string

## API Endpoints

- `POST /api/register`: Register a new user
- `POST /api/request-otp`: Request OTP for login
- `POST /api/verify-otp`: Verify OTP and get access token
- `GET /api/protected`: Protected endpoint requiring authentication
