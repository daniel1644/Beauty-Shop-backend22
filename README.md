## Beauty Shop
Beauty Shop is an e-commerce web application focused on selling beauty products. The project is built using Flask for the backend and React for the frontend. It provides a platform for customers to browse, purchase beauty products, and manage their orders. Admins have the ability to manage products, categories, and view order analytics.

## Table of Contents
Features
Project Structure
Setup and Installation
Running the Application
API Endpoints
Seeding the Database
Testing
Technologies Used
Contributing
License

## Features
# User Features:
User registration and login with JWT authentication.
Browse and search for beauty products by category.
Add products to cart and place orders.
View order history and status.

# Admin Features:
Add, update, and delete products and categories.
View and manage user orders.
View analytics of products and orders.

# Project Structure
beauty_shop/
│
├── app/
│   ├── resources
│   ├── __init__.py
│   ├── product.py
│   ├── auth.py
│   ├── order.py
│   ├── user.py
│   ├── cart.py
├── models.py
├── schemas.py
├── config.py
└── db.py
│
├── migrations/
│
├── seed.py
├── run.py
└── requirements.txt

## Setup and Installation
# Prerequisites
Python 3.8+
PostgreSQL
Node.js and npm (for frontend setup)

## Backend Setup
1. Clone the repository:
git clone https://github.com/yourusername/beauty_shop.git
cd beauty_shop

2. Create a virtual environment:
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`


3. Install dependencies:
pip install -r requirements.txt


4. Set up environment variables: Create a .env file and add the following environment variables:
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://myuser:mypassword@localhost/beauty_shop_db
JWT_SECRET_KEY=your_jwt_secret_key


5. Initialize the database: 
flask db init
flask db migrate
flask db upgrade

## Frontend Setup
The frontend is built using React. You can find the frontend code in the frontend/ directory.

1. Navigate to the frontend directory:
cd frontend

2. Install dependencies:
npm install


3. Start the frontend server:
npm start

## Running the Application
1. Start the backend server:
python run.py

2. Access the application:

Backend: http://localhost:5000/
Frontend: http://localhost:3000/


## API Endpoints
# Authentication
POST /register - Register a new user
POST /login - Login and retrieve JWT token

# Products
GET /products - Get all products
POST /products - Add a new product (Admin only)

# Orders
GET /orders - Get orders for the logged-in user
POST /orders - Create a new order

# Admin
GET /admin/orders - View all orders (Admin only)
PUT /admin/orders/<order_id> - Update order status (Admin only)

# Seeding the Database
To seed the database with initial data, run the following command:
python seed.py

This will populate the database with categories, users, products, and orders for testing purposes.

## Testing
# Backend Testing
Run the backend tests using unittest:
python -m unittest discover -s tests

# Frontend Testing
The frontend uses Jest for testing React components:
npm test

## Technologies Used
Backend: Flask, SQLAlchemy, Flask-Migrate, Flask-JWT-Extended, Flask-CORS
Frontend: React, Redux Toolkit, CSS
Database: PostgreSQL
Testing: Unittest (backend), Jest (frontend)
Deployment: Docker (optional), Heroku/AWS (optional)

## Contributing
Contributions are welcome! Please fork this repository and submit a pull request for review.

## License
This project is licensed under the MIT License. See the LICENSE file for details.





