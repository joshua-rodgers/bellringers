"""
Test script to verify routes are registered correctly
"""
from app import app

with app.test_client() as client:
    # List all registered routes
    print("=== Registered Routes ===")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint:50s} {rule.rule:50s} {list(rule.methods)}")

    print("\n=== Testing Routes ===")

    # Test main route
    response = client.get('/bellringers/')
    print(f"/bellringers/ - Status: {response.status_code}")

    # Test admin login
    response = client.get('/bellringers/admin/login')
    print(f"/bellringers/admin/login - Status: {response.status_code}")

    # Test admin dashboard (should redirect or 401)
    response = client.get('/bellringers/admin/dashboard')
    print(f"/bellringers/admin/dashboard - Status: {response.status_code}")

    # Test register endpoint
    response = client.post('/bellringers/api/register',
                          json={'handle': 'test-user-123'},
                          content_type='application/json')
    print(f"/bellringers/api/register - Status: {response.status_code}")
