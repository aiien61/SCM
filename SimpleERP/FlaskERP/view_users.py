from app import app, db, User

with app.app_context():
    users = User.query.all()

    if users:
        print('User Lists:')
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}")
    else:
        print("No users found in the database.")
