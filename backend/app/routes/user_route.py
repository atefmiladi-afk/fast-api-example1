from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import (
    consume_email_token,
    create_access_token,
    create_email_token,
    get_current_user,
    hash_password,
    verify_password,
)
from app.database import get_db
from app.email_service import send_reset_email, send_verification_email
from app.models import User
from app.schemas import (
    ForgotPasswordIn,
    MessageOut,
    ResendVerificationIn,
    ResetPasswordIn,
    Token,
    UserCreate,
    UserLogin,
    UserOut,
    VerifyEmailIn,
)

router = APIRouter(prefix="/api/auth", tags=["users"])


@router.post("/register", response_model=MessageOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        is_verified=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_email_token(db, user, "verify", hours=24)
    send_verification_email(user.email, token)
    return MessageOut(
        message="Account created. Check your email to verify before signing in.",
        email=user.email,
    )


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email before signing in.",
        )
    token = create_access_token(user.username)
    return Token(access_token=token, user=UserOut.model_validate(user))


@router.get("/me", response_model=UserOut)
def me(current: User = Depends(get_current_user)):
    return UserOut.model_validate(current)


@router.post("/verify-email", response_model=MessageOut)
def verify_email(payload: VerifyEmailIn, db: Session = Depends(get_db)):
    user = consume_email_token(db, payload.token, "verify")
    user.is_verified = True
    db.commit()
    return MessageOut(message="Email verified. You can now sign in.", email=user.email)


@router.post("/resend-verification", response_model=MessageOut)
def resend_verification(payload: ResendVerificationIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if user and not user.is_verified:
        token = create_email_token(db, user, "verify", hours=24)
        send_verification_email(user.email, token)
    return MessageOut(message="If that email exists and is not verified, a new link was sent.")


@router.post("/forgot-password", response_model=MessageOut)
def forgot_password(payload: ForgotPasswordIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if user:
        token = create_email_token(db, user, "reset", hours=1)
        send_reset_email(user.email, token)
    return MessageOut(message="If that email is registered, a reset link was sent.")


@router.post("/reset-password", response_model=MessageOut)
def reset_password(payload: ResetPasswordIn, db: Session = Depends(get_db)):
    user = consume_email_token(db, payload.token, "reset")
    user.hashed_password = hash_password(payload.password)
    db.commit()
    return MessageOut(message="Password updated. You can now sign in.", email=user.email)
