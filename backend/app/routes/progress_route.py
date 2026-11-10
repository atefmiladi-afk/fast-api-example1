from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import User, UserProgress, Word
from app.schemas import ProgressOut, ProgressUpdate

router = APIRouter(prefix="/api/progress", tags=["progress"])


@router.put("/{word_id}", response_model=ProgressOut)
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
