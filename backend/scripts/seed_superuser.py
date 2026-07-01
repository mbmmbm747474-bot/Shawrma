"""
One-time bootstrap script: creates the first Company, Branch, and a
superuser account so you can log in and use the API to create everything
else.

Why this exists: every "create company" / "create user" endpoint requires
an authenticated superuser, but a superuser must already belong to a
company. There is no way to get the very first account through the HTTP
API alone — this script breaks that chicken-and-egg problem.

Usage (from the backend/ directory, with DATABASE_URL pointing at a
migrated database):

    python -m scripts.seed_superuser

Or inside the running Docker container:

    docker compose exec backend python -m scripts.seed_superuser

It is safe to run more than once — it does nothing if a superuser with the
given username already exists.
"""
import getpass
import sys

from app.core.database import SessionLocal
from app.models.branch import Branch
from app.models.company import Company
from app.models.user import User
from app.security.hashing import hash_password


def main() -> None:
    db = SessionLocal()
    try:
        username = input("Superuser username [admin]: ").strip() or "admin"

        existing = db.query(User).filter(User.username == username).first()
        if existing:
            print(f"A user with username '{username}' already exists. Nothing to do.")
            return

        company_name = input("Company name [Default Company]: ").strip() or "Default Company"
        branch_name = input("Branch name [Main Branch]: ").strip() or "Main Branch"
        email = input("Superuser email [admin@example.com]: ").strip() or "admin@example.com"
        full_name = input("Superuser full name [Administrator]: ").strip() or "Administrator"

        password = getpass.getpass("Superuser password (min 8 chars): ")
        if len(password) < 8:
            print("Password must be at least 8 characters. Aborting.")
            sys.exit(1)
        password_confirm = getpass.getpass("Confirm password: ")
        if password != password_confirm:
            print("Passwords do not match. Aborting.")
            sys.exit(1)

        company = Company(name=company_name, currency="EGP")
        db.add(company)
        db.flush()  # get company.id without committing yet

        branch = Branch(company_id=company.id, name=branch_name)
        db.add(branch)
        db.flush()

        user = User(
            username=username,
            email=email,
            full_name=full_name,
            password_hash=hash_password(password),
            company_id=company.id,
            branch_id=branch.id,
            is_active=True,
            is_superuser=True,
        )
        db.add(user)
        db.commit()

        print()
        print("Done. Created:")
        print(f"  Company: {company.name} ({company.id})")
        print(f"  Branch:  {branch.name} ({branch.id})")
        print(f"  User:    {user.username} <{user.email}> (superuser)")
        print()
        print("You can now log in via POST /api/v1/auth/login with this username and password.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
