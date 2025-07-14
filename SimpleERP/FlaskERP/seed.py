from app import app, db, User
from werkzeug.security import generate_password_hash

# Ensure the database is set up
with app.app_context():
    # Checks if admin user already exists
    existing_user = User.query.filter_by(username='admin').first()
    
    if not existing_user:
        test_user = User(username='admin', password=generate_password_hash("admin123"))
        db.session.add(test_user)
        db.session.commit()
        print("Admin user created successfully!")
    else:
        print("Admin user already exists. Skipping insertion.")