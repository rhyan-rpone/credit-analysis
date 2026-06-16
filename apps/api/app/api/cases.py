from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models import CreditCase
from app.db.session import get_db
from app.schemas import CreditCaseCreate, CreditCaseRead

router = APIRouter(prefix="/cases", tags=["cases"])


@router.post("", response_model=CreditCaseRead)
def create_case(payload: CreditCaseCreate, db: Session = Depends(get_db)):
    case = CreditCase(
        company_name=payload.company_name,
        cnpj=payload.cnpj,
        requested_amount=payload.requested_amount,
    )
    db.add(case)
    db.commit()
    db.refresh(case)
    return case


@router.get("", response_model=list[CreditCaseRead])
def list_cases(db: Session = Depends(get_db)):
    return db.query(CreditCase).order_by(CreditCase.created_at.desc()).all()


@router.get("/{case_id}", response_model=CreditCaseRead)
def get_case(case_id: UUID, db: Session = Depends(get_db)):
    case = db.get(CreditCase, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case