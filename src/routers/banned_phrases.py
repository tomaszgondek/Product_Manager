from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db import get_db
from src.repositories.product_repository import BannedPhraseRepository

router = APIRouter(prefix="/api/v1/banned-phrases", tags=["banned_phrases"])

@router.get("/", status_code=status.HTTP_200_OK)
def list_phrases(db: Session = Depends(get_db)):
    repo = BannedPhraseRepository(db)
    phrases = repo.list()
    return [
        {
            "id": p.id,
            "phrase": p.phrase,
            "created_at": p.created_at.isoformat() if p.created_at else None
        }
        for p in phrases
    ]

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_phrase(payload: dict, db: Session = Depends(get_db)):
    repo = BannedPhraseRepository(db)
    phrase = payload.get("phrase") if isinstance(payload, dict) else None
    if not phrase:
        raise HTTPException(status_code=400, detail={"phrase": "Phrase is required"})
    if repo.get_by_phrase(phrase):
        raise HTTPException(status_code=400, detail={"phrase": "Phrase already exists"})
    new_phrase = repo.create(phrase)
    return {
        "id": new_phrase.id,
        "phrase": new_phrase.phrase,
        "created_at": new_phrase.created_at.isoformat() if new_phrase.created_at else None
    }

@router.delete("/{phrase_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_phrase(phrase_id: int, db: Session = Depends(get_db)):
    repo = BannedPhraseRepository(db)
    repo.delete(phrase_id)
    return
