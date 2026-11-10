from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Category, User, UserProgress, Word
from app.schemas import CategoryDetail, CategoryOut, WordOut

router = APIRouter(prefix="/api/categories", tags=["categories"])


def _learned_map(db: Session, user_id: int) -> dict[int, bool]:
    rows = db.query(UserProgress).filter(UserProgress.user_id == user_id).all()
    return {row.word_id: row.learned for row in rows}


@router.get("", response_model=list[CategoryOut])
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


@router.get("/{slug}", response_model=CategoryDetail)
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
