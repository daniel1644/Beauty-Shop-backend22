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

def seed_data():
    # Add accessory products
    accessories = [
        {'name': 'Hair rollers', 'image': 'https://i.pinimg.com/originals/94/26/53/9426534a94ef632cf5762f27b69bf985.jpg', 'category': 'Accessories', 'price': 10, 'description': 'Essential for perfect curls', 'stock': 100},
        {'name': 'Skin toner', 'image': 'https://i.pinimg.com/1200x/ca/7c/ae/ca7cae9f7e9f4fe512172b5bbd8331c8.jpg', 'category': 'Accessories', 'price': 15, 'description': 'Refreshes and balances skin', 'stock': 150},
        {'name': 'Moisturizing face mask', 'image': 'https://i.pinimg.com/originals/5d/c7/07/5dc707af23b776dd99336b36e4c4d21f.jpg', 'category': 'Accessories', 'price': 20, 'description': 'Hydrates and revitalizes skin', 'stock': 200},
        {'name': 'Nail polish remover', 'image': 'https://i.pinimg.com/originals/70/d5/d9/70d5d93a8debdcc4d6e91a5e46060b93.jpg', 'category': 'Accessories', 'price': 5, 'description': 'Removes nail polish effortlessly', 'stock': 250},
        {'name': 'Lip balm', 'image': 'https://i.pinimg.com/originals/69/70/4b/69704b2df6f8a87c00406b6b7349ea16.jpg', 'category': 'Accessories', 'price': 3, 'description': 'Keeps lips soft and hydrated', 'stock': 300},
        {'name': 'Eyebrow pencil', 'image': 'https://i.pinimg.com/originals/ce/2e/26/ce2e26c7401a67b440ebd8e23c742081.jpg', 'category': 'Accessories', 'price': 8, 'description': 'Defines and shapes eyebrows', 'stock': 120},
        {'name': 'Facial cleanser', 'image': 'https://i.pinimg.com/originals/d0/37/c0/d037c0a2679a5c53b8d2b0d39193c36d.jpg', 'category': 'Accessories', 'price': 12, 'description': 'Gently cleanses and purifies skin', 'stock': 180},
        {'name': 'Hand cream', 'image': 'https://i.pinimg.com/originals/54/9e/9e/549e9e7f0ac8825dc8e9b99a5cbbd482.jpg', 'category': 'Accessories', 'price': 7, 'description': 'Nourishes and softens hands', 'stock': 220},
        {'name': 'Shampoo brush', 'image': 'https://i.pinimg.com/originals/1c/47/c1/1c47c1648b7fcaf5a6d0fdad8d674f67.jpg', 'category': 'Accessories', 'price': 6, 'description': 'Enhances shampooing experience', 'stock': 130},
        {'name': 'Face roller', 'image': 'https://i.pinimg.com/originals/ae/7b/6c/ae7b6c740dce6c5507d4d9fa5d4998e7.jpg', 'category': 'Accessories', 'price': 18, 'description': 'Improves circulation and reduces puffiness', 'stock': 90}
    ]
    
    for accessory in accessories:
        product = Product(
            name=accessory['name'], 
            image=accessory['image'], 
            category=accessory['category'],
            price=accessory.get('price', 0),  # Default to 0 if not provided
            description=accessory.get('description', ''),  # Default to empty string if not provided
            stock=accessory.get('stock', 0)  # Default to 0 if not provided
        )
        db.session.add(product)

    db.session.commit()
    print("Accessory products added successfully.")



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
    image_paths = [
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg",
        "https://example.com/image3.jpg",
        # Add more image URLs here
    ]
    for _ in range(20):
        product = Product(
            name=fake.word(),
            price=fake.random_number(digits=2),
            description=fake.text(),
            category=fake.word(),
            stock=fake.random_number(digits=2),
            image=rc(image_paths)  # Assign a random image URL to each product
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
    
    # Call the function to seed accessory products
    seed_data()

    print("Complete.")
