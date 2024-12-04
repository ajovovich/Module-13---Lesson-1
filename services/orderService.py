from sqlalchemy.orm import Session
from database import db
from models.order import Order
from circuitbreaker import circuit
from sqlalchemy import select

def fallback_function(order):
    return None

@circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_function)
def save(order_data):
    try:
        if order_data['name'] == "failure":
            raise Exception("Failure condition triggered")
        with Session(db.engine) as session:
            with session.begin():
                new_order = Order(customer_id=order_data['customer_id'], product_id=order_data['product_id'], quantity=order_data['quantity'], total_price=order_data['total_price'])
                session.add(new_order)
                session.commit()
            session.refresh(new_order)
            return new_order
    
    except Exception as e:
        raise e

def find_all():
    query = select([Order])
    orders = db.session.execute(query).scalars().all()
    return orders

#Task 1:

def find_all_pagination(page=1, per_page=10):
    orders = db.paginate(select(Order), page=page, per_page=per_page)
    return orders