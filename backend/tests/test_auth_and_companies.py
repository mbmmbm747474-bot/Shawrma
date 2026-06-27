import uuid

from app.models.company import Company
from app.models.branch import Branch
from app.models.user import User
from app.security.hashing import hash_password


def _seed_company_branch_superuser(db_session):
    company = Company(name="Test Co", currency="EGP")
    db_session.add(company)
    db_session.commit()

    branch = Branch(company_id=company.id, name="Main Branch")
    db_session.add(branch)
    db_session.commit()

    user = User(
        username="admin",
        email="admin@example.com",
        full_name="Admin User",
        password_hash=hash_password("supersecret123"),
        company_id=company.id,
        branch_id=branch.id,
        is_superuser=True,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    return company, branch, user


def test_login_and_get_me(client, db_session):
    company, branch, user = _seed_company_branch_superuser(db_session)

    login_resp = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "supersecret123"},
    )
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]

    me_resp = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_resp.status_code == 200
    assert me_resp.json()["username"] == "admin"


def test_superuser_can_create_company(client, db_session):
    company, branch, user = _seed_company_branch_superuser(db_session)

    login_resp = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "supersecret123"},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create_resp = client.post(
        "/api/v1/companies/",
        json={"name": "New Branch Co", "currency": "EGP"},
        headers=headers,
    )
    assert create_resp.status_code == 201
    assert create_resp.json()["name"] == "New Branch Co"

    list_resp = client.get("/api/v1/companies/", headers=headers)
    assert list_resp.status_code == 200
    assert len(list_resp.json()) >= 2


def test_non_superuser_cannot_create_company(client, db_session):
    company = Company(name="Test Co 2", currency="EGP")
    db_session.add(company)
    db_session.commit()

    branch = Branch(company_id=company.id, name="Branch 2")
    db_session.add(branch)
    db_session.commit()

    user = User(
        username="staffuser",
        email="staff@example.com",
        full_name="Staff User",
        password_hash=hash_password("password123"),
        company_id=company.id,
        branch_id=branch.id,
        is_superuser=False,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    login_resp = client.post(
        "/api/v1/auth/login",
        data={"username": "staffuser", "password": "password123"},
    )
    token = login_resp.json()["access_token"]

    create_resp = client.post(
        "/api/v1/companies/",
        json={"name": "Should Not Be Created", "currency": "EGP"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert create_resp.status_code == 403
