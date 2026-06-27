def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_openapi_schema_loads(client):
    response = client.get("/api/v1/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "paths" in schema
    # spot-check that the milestone-1 routers are actually mounted
    assert "/api/v1/auth/login" in schema["paths"]
    assert "/api/v1/users/" in schema["paths"]
    assert "/api/v1/companies/" in schema["paths"]
    assert "/api/v1/branches/" in schema["paths"]
    assert "/api/v1/roles/" in schema["paths"]
    assert "/api/v1/dashboard/summary" in schema["paths"]


def test_login_requires_valid_credentials(client):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "doesnotexist", "password": "wrong"},
    )
    assert response.status_code == 400


def test_protected_endpoint_requires_auth(client):
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401
