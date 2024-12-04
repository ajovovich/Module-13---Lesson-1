from sqlalchemy.orm import Session
from database import db
from models.product import Product
from models.order import Order
from circuitbreaker import circuit
from sqlalchemy import select, func

def fallback_function(product):
    return None

@circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_function)
def save(product_data):
    try:
        if product_data['name'] == "failure":
            raise Exception("Failure condition triggered")
        with Session(db.engine) as session:
            with session.begin():
                new_product = Product(name=product_data['name'], price=product_data['price'])
                session.add(new_product)
                session.commit()
            session.refresh(new_product)
            return new_product
    
    except Exception as e:
        raise e

def find_all():
    query = select([Product])
    products = db.session.execute(query).scalars().all()
    return products

#Task 2:

def find_all_pagination(page=1, per_page=10):
    products = db.paginate(select(Product), page=page, per_page=per_page)
    return products

#Task 2: Part 2

def identify_top_selling_products():
    results = (
        db.session.query(Product.name, func.sum(Order.quantity))
        .join(Order, Product.id == Order.product_id)
        .group_by(Product.name)
        .order_by(func.sum(Order.quantity).desc())
        .all()
    )
    return results