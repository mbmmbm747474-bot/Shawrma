"""Desktop-mode startup bootstrap.

Runs automatically when the bundled desktop backend starts (see
desktop_main.py). Unlike scripts/seed_superuser.py (interactive, for the
Docker/server setup), this is fully automatic - there is no terminal for
the user to type into in the packaged app.

On first launch (empty database):
  - Creates every table directly from the SQLAlchemy models, via
    Base.metadata.create_all(). This intentionally does NOT use Alembic -
    the desktop build has no migration history to manage, it just needs
    the current schema to exist. The Docker/Postgres deployment keeps
    using real Alembic migrations (see alembic/versions/) untouched.
  - Creates one Company, one Branch, and one superuser with a fixed,
    well-known default password, then writes that password to a text
    file next to the database so the user can find it.

On subsequent launches, all of this is a no-op: tables already exist,
and a superuser already exists, so nothing is recreated.
"""
from __future__ import annotations

import secrets
from pathlib import Path

from app.core.database import SessionLocal, engine
from app.models.base import Base
from app.models.branch import Branch
from app.models.company import Company
from app.models.user import User
from app.security.hashing import hash_password

DEFAULT_USERNAME = "admin"
DEFAULT_COMPANY_NAME = "مطعمي"
DEFAULT_BRANCH_NAME = "الفرع الرئيسي"


def _generate_password() -> str:
    # Short enough to type/read comfortably, long enough to not be a joke.
    # This is a local single-user desktop demo, not an internet-facing
    # deployment - see the README caveat about not using this build for that.
    return secrets.token_urlsafe(9)


def bootstrap(data_dir: Path) -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        existing_admin = db.query(User).filter(User.username == DEFAULT_USERNAME).first()
        if existing_admin:
            return  # already bootstrapped, nothing to do

        company = Company(name=DEFAULT_COMPANY_NAME, currency="EGP")
        db.add(company)
        db.flush()

        branch = Branch(company_id=company.id, name=DEFAULT_BRANCH_NAME)
        db.add(branch)
        db.flush()

        password = _generate_password()

        admin = User(
            username=DEFAULT_USERNAME,
            email="admin@local.app",
            full_name="مدير النظام",
            password_hash=hash_password(password),
            company_id=company.id,
            branch_id=branch.id,
            is_active=True,
            is_superuser=True,
        )
        db.add(admin)
        db.commit()

        credentials_file = data_dir / "بيانات-الدخول.txt"
        credentials_file.write_text(
            "بيانات تسجيل الدخول لأول مرة\n"
            "----------------------------\n"
            f"اسم المستخدم: {DEFAULT_USERNAME}\n"
            f"كلمة المرور: {password}\n\n"
            "يمكنك تغيير كلمة المرور من داخل التطبيق بعد تسجيل الدخول.\n"
            "احتفظ بهذا الملف في مكان آمن أو احذفه بعد تذكر كلمة المرور.\n",
            encoding="utf-8",
        )
    finally:
        db.close()
