from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from .. import models

router = APIRouter()

# 1. GET /analytics/total-sales - Calculate total revenue
@router.get("/total-sales")
def get_total_sales(db: Session = Depends(get_db)):
    """
    Calculates total sales based on price * quantity for all transactions.
    [Requirement: source 44]
    """
    # SQL equivalent: SELECT SUM(price * quantity) FROM transactions
    total_sales = db.query(
        func.sum(models.Transaction.price * models.Transaction.quantity)
    ).scalar() or 0.0
    
    return {"total_sales": round(total_sales, 2)}

# 2. GET /analytics/top-properties - Top 3 by revenue
@router.get("/top-properties")
def get_top_properties(db: Session = Depends(get_db)):
    """
    Returns the top 3 properties based on total revenue.
    [Requirement: source 45]
    """
    # Group by property_name, sum revenue, sort descending, limit to 3
    results = db.query(
        models.Transaction.property_name,
        func.sum(models.Transaction.price * models.Transaction.quantity).label("revenue")
    ).group_by(models.Transaction.property_name)\
     .order_by(func.sum(models.Transaction.price * models.Transaction.quantity).desc())\
     .limit(3)\
     .all()

    # Format the output into a clean list of dictionaries
    top_list = [
        {"property_name": row[0], "total_revenue": round(row[1], 2)} 
        for row in results
    ]
    
    return top_list