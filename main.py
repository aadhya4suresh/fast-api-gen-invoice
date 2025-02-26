from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field, condecimal, validator
from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from models import Project as DBProject, Billing as DBBilling, SessionLocal  # Ensure these models are defined correctly
from sqlalchemy import select

app = FastAPI()

# Project model for input validation
class Project(BaseModel):
    project_name: str
    client_name: str
    address: str
    post_code: str
    country: str
    billing_type: str = Field(..., pattern='^(hourly|monthly|fixed-bid)$')
    contract_status: str = Field(..., pattern='^(active|inactive)$')
    start_date: str
    end_date: Optional[str] = None
    hourly_price: Optional[condecimal(ge=0)] = None  # Allow zero
    fixed_price: Optional[condecimal(ge=0)] = None   # Allow zero

    @validator('start_date')
    def validate_start_date(cls, v: str) -> datetime:
        try:
            return datetime.strptime(v, '%d-%m-%Y')
        except ValueError:
            raise ValueError('start_date must be in the format dd-mm-yyyy')

    @validator('end_date', always=True)
    def validate_end_date(cls, v: Optional[str]) -> Optional[datetime]:
        if v == "" or v is None:
            return None
        try:
            return datetime.strptime(v, '%d-%m-%Y')
        except ValueError:
            raise ValueError('end_date must be in the format dd-mm-yyyy')

    @validator('fixed_price', always=True)
    def validate_fixed_price(cls, v: Optional[float], values: dict) -> Optional[float]:
        billing_type = values.get('billing_type')
        if billing_type == "hourly" and v is not None and v > 0:
            raise ValueError("fixed_price must be zero when billing_type is 'hourly'")
        if billing_type == "monthly" and (v is None or v <= 0):
            raise ValueError("fixed_price must be greater than 0 when billing_type is 'monthly'")
        return v

    @validator('hourly_price', always=True)
    def validate_hourly_price(cls, v: Optional[float], values: dict) -> Optional[float]:
        billing_type = values.get('billing_type')
        if billing_type == "fixed-bid" and v is not None and v > 0:
            raise ValueError("hourly_price must be zero when billing_type is 'fixed-bid'")
        if billing_type == "monthly" and (v is None or v <= 0):
            raise ValueError("hourly_price must be greater than 0 when billing_type is 'monthly'")
        if billing_type == "hourly" and (v is None or v <= 0):
            raise ValueError("hourly_price must be provided and greater than 0 when billing_type is 'hourly'")
        return v

# Billing model for input validation
class Billing(BaseModel):
    project_id: int
    allocated_resource: str
    month_of_billing: str  # Format: 'YYYY-MM'
    year_of_billing: int    # New field
    total_hours: condecimal(gt=0)  # Must be greater than 0
    description: Optional[str] = None

# Billing summary model for output
class BillingSummary(BaseModel):
    project_name: str
    resource_name: str
    total_amount_usd: condecimal(gt=0)
    month: int
    year: int

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/projects/")
def create_project(project: Project, db: Session = Depends(get_db)):
    new_project = DBProject(**project.dict())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return {"message": "Project created successfully!", "project": new_project}

@app.post("/create-billing/")
def create_billing(billing: Billing, db: Session = Depends(get_db)):
    # Check if the project_id exists
    project = db.query(DBProject).filter(DBProject.id == billing.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    new_billing = DBBilling(**billing.dict())
    db.add(new_billing)
    db.commit()
    db.refresh(new_billing)
    return {"message": "Billing created successfully!", "billing": new_billing}

@app.post("/calculate-monthly-billing/", response_model=List[BillingSummary])
def calculate_monthly_billing(month: str, db: Session = Depends(get_db)):
    results = []
    billings = db.query(DBBilling).filter(DBBilling.month_of_billing == month).all()

    for billing in billings:
        project = db.query(DBProject).filter(DBProject.id == billing.project_id).first()
        if project:
            total_amount = 0
            if project.billing_type == 'hourly':
                total_amount = billing.total_hours * project.hourly_price
            results.append(BillingSummary(
                project_name=project.project_name,
                resource_name=billing.allocated_resource,
                total_amount_usd=total_amount,
                month=int(month.split('-')[1]),
                year=billing.year_of_billing  # Use year_of_billing here
            ))

    return results

# Optional: Endpoint to retrieve all projects
@app.get("/projects/")
def get_projects(db: Session = Depends(get_db)):
    return db.query(DBProject).all()

# Optional: Endpoint to retrieve all billings
@app.get("/billings/")
def get_billings(db: Session = Depends(get_db)):
    return db.query(DBBilling).all()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
