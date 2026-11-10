from datetime import datetime, timedelta
import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import EmailToken, User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(subject: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({"sub": subject, "exp": expire}, settings.secret_key, algorithm=settings.algorithm)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str | None = payload.get("sub")
        if not username:
            raise credentials_error
    except JWTError:
        raise credentials_error
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise credentials_error
    return user


def create_email_token(db: Session, user: User, purpose: str, hours: int) -> str:
    db.query(EmailToken).filter(
        EmailToken.user_id == user.id,
        EmailToken.purpose == purpose,
        EmailToken.used.is_(False),
    ).update({"used": True})
    token = secrets.token_urlsafe(32)
    row = EmailToken(
        user_id=user.id,
        token=token,
        purpose=purpose,
        expires_at=datetime.utcnow() + timedelta(hours=hours),
        used=False,
    )
    db.add(row)
    db.commit()
    return token


def consume_email_token(db: Session, token: str, purpose: str) -> User:
    row = db.query(EmailToken).filter(EmailToken.token == token, EmailToken.purpose == purpose).first()
    if not row or row.used or row.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    row.used = True
    db.commit()
    user = db.query(User).filter(User.id == row.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    return user
