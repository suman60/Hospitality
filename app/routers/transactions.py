from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from .auth import get_current_user
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
import csv
import io

from ..database import get_db
from .. import models, schemas

router = APIRouter()

# 1. POST /transactions - Add Single Data
@router.post("/", response_model=schemas.Transaction)
def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# 2. POST /transactions/bulk - Bulk Upload (JSON) 
@router.post("/bulk", response_model=List[schemas.Transaction])
def create_transactions_bulk(transactions: List[schemas.TransactionCreate], db: Session = Depends(get_db)):
    db_txs = [models.Transaction(**tx.dict()) for tx in transactions]
    db.add_all(db_txs)
    db.commit()
    # Refreshing all objects to return them with IDs
    for tx in db_txs:
        db.refresh(tx)
    return db_txs

# 3. POST /transactions/upload-csv - CSV Upload
@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV") 

    content = await file.read()
    stream = io.StringIO(content.decode('utf-8'))
    reader = csv.DictReader(stream)
    
    new_transactions = []
    try:
        for row in reader:
            # Logic to parse CSV rows into the database model 
            tx = models.Transaction(
                property_name=row['property_name'],
                category=row['category'],
                price=float(row['price']),
                quantity=int(row['quantity']),
                date=date.fromisoformat(row['date'])
            )
            new_transactions.append(tx)
        
        db.add_all(new_transactions)
        db.commit()
        return {"message": f"Successfully uploaded {len(new_transactions)} transactions"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Error parsing CSV: {str(e)}") 

# 4. GET /transactions - View with Filters 
@router.get("/", response_model=List[schemas.Transaction])
def read_transactions(
    category: Optional[str] = None, 
    start_date: Optional[date] = None, 
    end_date: Optional[date] = None, 
    db: Session = Depends(get_db)
):
    query = db.query(models.Transaction)
    
    if category:
        query = query.filter(models.Transaction.category == category) 
    if start_date:
        query = query.filter(models.Transaction.date >= start_date) 
    if end_date:
        query = query.filter(models.Transaction.date <= end_date) 
        
    return query.all()