"""
Database initialization script
Run this once to set up the database
"""
import hashlib
from database import init_db, create_admin
from config import Config


def setup_database():
    """Initialize database and create default admin user"""
    print("Initializing database...")
    init_db()
    print("Database tables created successfully!")

    # Create default admin user
    username = Config.DEFAULT_ADMIN_USERNAME
    password = Config.DEFAULT_ADMIN_PASSWORD
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    if create_admin(username, password_hash):
        print(f"Admin user '{username}' created successfully!")
        print(f"Default password: {password}")
        print("IMPORTANT: Change the admin password after first login!")
    else:
        print(f"Admin user '{username}' already exists.")

    print("\nDatabase setup complete!")


if __name__ == '__main__':
    setup_database()
