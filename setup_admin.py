from app.app import create_app
from app.models import db, User

app = create_app()
with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        print("Creating admin user...")
        admin = User(username='admin', email='admin@safelink.com', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully (username: admin, password: admin123)")
    else:
        print("Admin user already exists. Resetting password to admin123...")
        admin.set_password('admin123')
        admin.is_admin = True
        db.session.commit()
        print("Admin password reset successfully.")
