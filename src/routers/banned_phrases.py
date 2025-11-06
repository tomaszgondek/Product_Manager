from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from db import get_db
from repositories.product_repository import BannedPhraseRepository
from schemas import BannedPhraseCreate, BannedPhraseOut

router = APIRouter(prefix="/api/v1/banned-phrases", tags=["banned_phrases"])

@router.post("/", response_model=BannedPhraseOut, status_code=status.HTTP_201_CREATED)
def add_phrase(payload: BannedPhraseCreate, db: Session = Depends(get_db)):
    repo = BannedPhraseRepository(db)
    existing = repo.get_by_phrase(payload.phrase)
    if existing:
        raise HTTPException(status_code=400, detail="Phrase already exists")
    return repo.create(payload.phrase)

@router.get("/", response_model=List[BannedPhraseOut])
def list_phrases(db: Session = Depends(get_db)):
    repo = BannedPhraseRepository(db)
    return repo.list()

@router.delete("/{phrase_id}", status_code=204)
def delete_phrase(phrase_id: int, db: Session = Depends(get_db)):
    repo = BannedPhraseRepository(db)
    repo.delete(phrase_id)
    return