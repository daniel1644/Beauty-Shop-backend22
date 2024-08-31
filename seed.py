#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import create_app, db
from app.models import User, Product, Order, OrderItem, CartItem

fake = Faker()

app = create_app()

with app.app_context():
    # Create tables if they don't exist
    db.create_all()

    print("Deleting all records...")
    User.query.delete()
    Product.query.delete()
    Order.query.delete()
    OrderItem.query.delete()
    CartItem.query.delete()

    print("Creating users...")
    users = []
    for _ in range(10):
        user = User(username=fake.user_name(), email=fake.email(), password=fake.password())
        db.session.add(user)
        users.append(user)

    print("Creating products...")
    products = []
    for _ in range(20):
        product = Product(
            name=fake.word(),
            price=fake.random_number(digits=2),
            description=fake.text(),
            category=fake.word(),
            stock=fake.random_number(digits=2)
        )
        db.session.add(product)
        products.append(product)

    db.session.commit()  # Commit users and products before creating orders

    print("Creating orders and order items...")
    for user in users:
        order = Order(
            user_id=user.id,
            total=fake.random_number(digits=2)
        )
        db.session.add(order)
        db.session.commit()  # Commit the order to ensure its ID is available

        for _ in range(3):  # Add 3 items per order
            product = rc(products)
            if product:  # Ensure product is not None
                order_item = OrderItem(
                    product_id=product.id,
                    order_id=order.id,
                    quantity=fake.random_number(digits=2)
                )
                db.session.add(order_item)

    print("Creating cart items...")
    for user in users:
        product = rc(products)
        if product:  # Ensure product is not None
            cart_item = CartItem(
                product_id=product.id,
                quantity=fake.random_number(digits=2),
                user_id=user.id
            )
            db.session.add(cart_item)

    db.session.commit()
    print("Complete.")
