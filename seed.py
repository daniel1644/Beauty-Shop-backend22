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
        {'name': 'Moisturizing face mask', 'image': 'https://thebioaqua.com/cdn/shop/products/7_8e9b4b41-2499-460a-b183-4d482ef06f0d.jpg?v=1661831435&width=1445', 'category': 'Accessories', 'price': 20, 'description': 'Hydrates and revitalizes skin', 'stock': 200},
        {'name': 'Nail polish remover', 'image': 'https://goldengirlcosmetics.com/cdn/shop/products/NailEnamelRemover-60ml-Front.jpg?v=1693328930', 'category': 'Accessories', 'price': 5, 'description': 'Removes nail polish effortlessly', 'stock': 250},
        {'name': 'Lip balm', 'image': 'https://www.muastore.co.uk/cdn/shop/files/Hydra-Juice-Peptide-Lip-Balm-Berry-Bliss-LID-OFF_1800x1800.jpg?v=1707720522', 'category': 'Accessories', 'price': 3, 'description': 'Keeps lips soft and hydrated', 'stock': 300},
        {'name': 'Eyebrow pencil', 'image': 'https://media.allure.com/photos/6279456fcf77efb74699598f/3:2/w_3000,h_2000,c_limit/5-09%20brow%20pencils.jpg', 'category': 'Accessories', 'price': 8, 'description': 'Defines and shapes eyebrows', 'stock': 120},
        {'name': 'Facial cleanser', 'image': 'https://ke.jumia.is/unsafe/fit-in/680x680/filters:fill(white)/product/61/7796771/1.jpg?8908', 'category': 'Accessories', 'price': 12, 'description': 'Gently cleanses and purifies skin', 'stock': 180},
        {'name': 'Hand cream', 'image': 'https://cinnabargreen.com/app/uploads/2017/09/HANDCREAM.50ml.jpg', 'category': 'Accessories', 'price': 7, 'description': 'Nourishes and softens hands', 'stock': 220},
        {'name': 'Shampoo brush', 'image': 'https://cdn.shopify.com/s/files/1/0243/8817/3888/products/ShampooBrush_b2822665-3f1f-4a59-8d5d-c4ca6328051c.jpg?v=1644832303', 'category': 'Accessories', 'price': 6, 'description': 'Enhances shampooing experience', 'stock': 130},
        {'name': 'Face roller', 'image': 'https://bopowomen.com/cdn/shop/products/Rose-Quartz-Crystal-Facial-Roller.jpg?v=1653266208', 'category': 'Accessories', 'price': 18, 'description': 'Improves circulation and reduces puffiness', 'stock': 90}
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
        "https://media-cldnry.s-nbcnews.com/image/upload/rockcms/2024-06/240610-beauty-awards-2024-face-makeup-winners-vl-social-74fb90.jpg",
        "https://www.rarebeauty.com/cdn/shop/files/gnav-shop-dropdown-body-400x400_400x.jpg?v=1702303892",
        "https://assets.beautyhub.co.ke/wp-content/uploads/2024/03/29151351/beauty_of_joseon_glow_set.jpg",
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