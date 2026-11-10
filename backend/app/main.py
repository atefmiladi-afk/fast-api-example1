from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.auth import create_access_token, get_current_user, hash_password, verify_password
from app.database import Base, engine, get_db
from app.models import Category, User, UserProgress, Word
from app.schemas import (
    CategoryDetail,
    CategoryOut,
    ProgressOut,
    ProgressUpdate,
    Token,
    UserCreate,
    UserLogin,
    UserOut,
    WordOut,
)
from app.seed import seed_if_empty

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Deutsch Lernen", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    db = next(get_db())
    try:
        seed_if_empty(db)
    finally:
        db.close()


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/auth/register", response_model=Token)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(user.username)
    return Token(access_token=token, user=UserOut.model_validate(user))


@app.post("/api/auth/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    token = create_access_token(user.username)
    return Token(access_token=token, user=UserOut.model_validate(user))


@app.get("/api/auth/me", response_model=UserOut)
def me(current: User = Depends(get_current_user)):
    return UserOut.model_validate(current)


def _learned_map(db: Session, user_id: int) -> dict[int, bool]:
    rows = db.query(UserProgress).filter(UserProgress.user_id == user_id).all()
    return {row.word_id: row.learned for row in rows}


@app.get("/api/categories", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    categories = db.query(Category).order_by(Category.id).all()
    learned = (
        db.query(Word.category_id, func.count(UserProgress.id))
        .join(UserProgress, UserProgress.word_id == Word.id)
        .filter(UserProgress.user_id == current.id, UserProgress.learned.is_(True))
        .group_by(Word.category_id)
        .all()
    )
    learned_by_cat = {cid: count for cid, count in learned}
    result = []
    for cat in categories:
        result.append(
            CategoryOut(
                id=cat.id,
                slug=cat.slug,
                name_de=cat.name_de,
                name_en=cat.name_en,
                description=cat.description,
                emoji=cat.emoji,
                color=cat.color,
                image_url=cat.image_url,
                word_count=len(cat.words),
                learned_count=learned_by_cat.get(cat.id, 0),
            )
        )
    return result


@app.get("/api/categories/{slug}", response_model=CategoryDetail)
def get_category(slug: str, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    cat = db.query(Category).filter(Category.slug == slug).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    progress = _learned_map(db, current.id)
    words = [
        WordOut(
            id=w.id,
            german=w.german,
            article=w.article,
            english=w.english,
            example_de=w.example_de,
            example_en=w.example_en,
            image_url=w.image_url,
            audio_hint=w.audio_hint,
            learned=progress.get(w.id, False),
        )
        for w in cat.words
    ]
    return CategoryDetail(
        id=cat.id,
        slug=cat.slug,
        name_de=cat.name_de,
        name_en=cat.name_en,
        description=cat.description,
        emoji=cat.emoji,
        color=cat.color,
        image_url=cat.image_url,
        word_count=len(words),
        learned_count=sum(1 for w in words if w.learned),
        words=words,
    )


@app.put("/api/progress/{word_id}", response_model=ProgressOut)
def update_progress(
    word_id: int,
    payload: ProgressUpdate,
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
):
    word = db.query(Word).filter(Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    row = (
        db.query(UserProgress)
        .filter(UserProgress.user_id == current.id, UserProgress.word_id == word_id)
        .first()
    )
    if not row:
        row = UserProgress(user_id=current.id, word_id=word_id, learned=payload.learned)
        db.add(row)
    else:
        row.learned = payload.learned
    db.commit()
    return ProgressOut(word_id=word_id, learned=row.learned)
