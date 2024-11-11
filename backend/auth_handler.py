"""
This handles user authentication. If the user exists with a valid token, 
it returns the existing token to avoid duplication,
otherwise, it creates a new token.
"""

from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt
from sqlalchemy.orm import Session
from models import User, UserAuthentication

# Password hashing context
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# JWT configuration
# WARNING: This key is not secure, and also should be kept private!
# This key is for demonstration purposes only!
SECRET_KEY = "your-secret-key" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 600

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def login(db: Session, username: str, password: str):
    # Step 1: Authenticate user credentials
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        # If authentication failed
        return None

    # Step 2: Check if an existing token exists for the user
    existing_auth = db.query(UserAuthentication).filter(UserAuthentication.user_id == user.id).first()
    if existing_auth:
        # Return the existing token
        return existing_auth.auth_token

    # Step 3: Create a new token if none exists
    token_data = {"sub": user.username}
    token = create_access_token(data=token_data)
    new_auth = UserAuthentication(user_id=user.id, auth_token=token)
    db.add(new_auth)
    db.commit()
    db.refresh(new_auth)
    
    return new_auth.auth_token
