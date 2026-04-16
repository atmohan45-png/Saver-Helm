from app.app import create_app
from flask import render_template
from app.models import db, User

app = create_app()
with app.app_context():
    print("Testing template rendering...")
    users = User.query.all()
    try:
        render_template('admin.html', users=users)
        print("admin.html rendered successfully.")
    except Exception as e:
        print(f"admin.html rendering FAILED: {e}")

    try:
        render_template('dashboard.html', name="Test")
        print("dashboard.html rendered successfully.")
    except Exception as e:
        print(f"dashboard.html rendering FAILED: {e}")
