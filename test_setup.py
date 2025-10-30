"""
Quick test to verify the setup works
"""
import os
import sys

# Test imports
print("Testing imports...")
try:
    from bellringers import database as db
    from bellringers.config import Config
    from bellringers import gemini_api
    print("✓ All imports successful")
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

# Test database initialization
print("\nTesting database initialization...")
try:
    db.init_db()
    print("✓ Database initialized")
except Exception as e:
    print(f"✗ Database error: {e}")
    sys.exit(1)

# Test user creation
print("\nTesting user creation...")
try:
    test_handle = "test-user-001"
    if db.create_user(test_handle):
        print(f"✓ User '{test_handle}' created")
    else:
        print(f"✓ User already exists (expected on re-run)")
except Exception as e:
    print(f"✗ User creation error: {e}")
    sys.exit(1)

# Test options
print("\nTesting Gemini API options...")
try:
    topics = gemini_api.get_topic_options()
    formats = gemini_api.get_format_options()
    constraints = gemini_api.get_constraint_options()
    print(f"✓ Topics: {len(topics)}")
    print(f"✓ Formats: {len(formats)}")
    print(f"✓ Constraints: {len(constraints)}")
except Exception as e:
    print(f"✗ Options error: {e}")
    sys.exit(1)

# Test admin creation
print("\nTesting admin user creation...")
try:
    import hashlib
    test_admin_hash = hashlib.sha256("testpass".encode()).hexdigest()
    if db.create_admin("testadmin", test_admin_hash):
        print("✓ Admin user created")
    else:
        print("✓ Admin already exists (expected on re-run)")
except Exception as e:
    print(f"✗ Admin creation error: {e}")
    sys.exit(1)

# Test stats
print("\nTesting statistics...")
try:
    stats = db.get_activity_summary()
    print(f"✓ Total users: {stats['total_users']}")
    print(f"✓ Total bell ringers: {stats['total_bell_ringers']}")
except Exception as e:
    print(f"✗ Stats error: {e}")
    sys.exit(1)

print("\n" + "="*50)
print("✓ ALL TESTS PASSED!")
print("="*50)
print("\nYour Bell Ringers app is ready to run!")
print("\nTo start the app:")
print("1. Set environment variable: export GEMINI_API_KEY='your_key_here'")
print("2. Run: python app.py")
print("3. Open: http://localhost:5000")
