from app.app import create_app
from app.models import db, User

app = create_app()
with app.app_context():
    print("Checking database schema...")
    try:
        users = User.query.all()
        print(f"Found {len(users)} users.")
        for u in users:
            print(f"User: {u.username}, Email: {u.email}, Admin: {u.is_admin}")
    except Exception as e:
        print(f"ERROR: {e}")
