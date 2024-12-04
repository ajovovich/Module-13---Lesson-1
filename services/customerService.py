from sqlalchemy.orm import Session
from database import db
from models.customer import Customer
from models.order import Order
from circuitbreaker import circuit
from sqlalchemy import select, func

def fallback_function(customer):
    return None

@circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_function)
def save(customer_data):
    try:
        if customer_data['namer'] == "failure":
            raise Exception("Failure condition triggered")
        with Session(db.engine) as session:
            with session.begin():
                new_customer = Customer(name=customer_data['name'], phone=customer_data['phone'], email=customer_data['email'])
                session.add(new_customer)
                session.commit()
            session.refresh(new_customer)
            return new_customer
    
    except Exception as e:
        raise e

def find_all():
    query = select([Customer])
    customers = db.session.execute(query).scalars().all()
    return customers

#Task 3: Part 2

def determine_customer_lifetime_value(threshold=1000):
    results = (
        db.session.query(Customer.name, func.sum(Order.total_value))
        .join(Order, Customer.id == Order.customer_id)
        .group_by(Customer.name)
        .having(func.sum(Order.total_value) >= threshold)
        .all()
    )
    return results