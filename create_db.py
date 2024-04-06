from app import app, db

# Ensure that db.create_all() is called within the application context
with app.app_context():
    db.create_all()