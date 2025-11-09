from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
import os

Base = declarative_base()

class Vendor(Base):
    __tablename__ = "vendor"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

# Choose the correct line_items column:
USE_POSTGRES = os.getenv('USE_POSTGRES', '0') == '1'
if USE_POSTGRES:
    from sqlalchemy.dialects.postgresql import JSONB
    line_items_type = JSONB
else:
    from sqlalchemy.types import JSON
    line_items_type = JSON

class Invoice(Base):
    __tablename__ = "invoice"
    id = Column(Integer, primary_key=True)
    vendor_id = Column(Integer, ForeignKey('vendor.id'))
    vendor = relationship('Vendor')
    invoice_no = Column(String, nullable=False)
    invoice_date = Column(Date)
    amount = Column(Float)
    currency = Column(String(4))
    line_items = Column(line_items_type)
    confidence = Column(Float)
    parsed_at = Column(Date)
