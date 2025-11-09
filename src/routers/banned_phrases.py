from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from src.db import get_db
from src.repositories.product_repository import BannedPhraseRepository

router = APIRouter(prefix="/api/v1/banned-phrases", tags=["banned_phrases"])

@router.get("/", response_model=List[dict])
def list_phrases(db: Session = Depends(get_db)):
    repo = BannedPhraseRepository(db)
    return repo.list()

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_phrase(payload: dict, db: Session = Depends(get_db)):
    repo = BannedPhraseRepository(db)
    phrase = payload.get("phrase") if isinstance(payload, dict) else None
    if not phrase:
        raise HTTPException(status_code=400, detail={"phrase":"Phrase is required"})
    if repo.get_by_phrase(phrase):
        raise HTTPException(status_code=400, detail={"phrase":"Phrase already exists"})
    return repo.create(phrase)

@router.delete("/{phrase_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_phrase(phrase_id: int, db: Session = Depends(get_db)):
    repo = BannedPhraseRepository(db)
    repo.delete(phrase_id)
    return
