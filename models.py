from sqlalchemy import Column, Integer, String, Float, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String, index=True)
    client_name = Column(String)  # New field
    address = Column(String)       # New field
    post_code = Column(String)     # New field
    country = Column(String)       # New field
    billing_type = Column(String)
    contract_status = Column(String)
    start_date = Column(String)    # Consider changing to Date if appropriate
    end_date = Column(String, nullable=True)  # Consider changing to Date if appropriate
    hourly_price = Column(Float, nullable=True)
    fixed_price = Column(Float, nullable=True)

class Billing(Base):
    __tablename__ = 'billings'

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    allocated_resource = Column(String)
    month_of_billing = Column(String)
    year_of_billing = Column(Integer)  # New field
    total_hours = Column(Float)
    description = Column(String, nullable=True)

# Create a SQLite database
DATABASE_URL = "sqlite:///./invoice-qa.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
