# run.py
from app import create_app, db, app
from dotenv import load_dotenv
load_dotenv()

# app = create_app()

def init_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(port=5000, debug=True)
