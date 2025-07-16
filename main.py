from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
import uvicorn

from models import Complaint, engine, SessionLocal, Base
from sentiment import analyze_sentiment
from geo import get_location
from category import get_complaint_category

app = FastAPI()

Base.metadata.create_all(bind=engine)


class ComplaintRequest(BaseModel):
    text: str


@app.post('/complaints', summary='Определение тональности текста')
def create_complaint(complaint: ComplaintRequest, request: Request):
    db: Session = SessionLocal()

    # Анализ тональности
    try:
        sentiment = analyze_sentiment(complaint.text)
    except Exception:
        sentiment = 'unknown'

    # Определение категории через GPT-3.5 Turbo
    category = get_complaint_category(complaint.text)

    # Определение локации
    try:
        ip = request.client.host
        location = get_location(ip)
    except Exception:
        location = 'unknown'

    # Запись в БД
    new_complaint = Complaint(
        text=complaint.text,
        sentiment=sentiment,
        status='open',
        timestamp=datetime.utcnow(),
        category=category
    )
    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)

    return {
        "id": new_complaint.id,
        "status": new_complaint.status,
        "sentiment": new_complaint.sentiment,
        "category": new_complaint.category,
        'location': location
    }


@app.get('/complaints')
def get_complaints():
    db: Session = SessionLocal()
    return db.query(Complaint).all()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    
