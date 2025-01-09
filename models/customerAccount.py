from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import List
from models.customer import Customer 

class CustomerAccount(Base):
    __tablename__ = 'customer_accounts'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customer.id'))  # Referencing table name explicitly
    customer: Mapped["Customer"] = db.relationship(back_populates='customer_account', lazy="noload")
    roles: Mapped[List["Role"]] = db.relationship(secondary="Customer_Management_Roles")