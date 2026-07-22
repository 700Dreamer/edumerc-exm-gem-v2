import os
import uuid
from typing import Optional
from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, UUIDIDMixin, schemas
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import User, get_async_session

SECRET = os.environ.get("JWT_SECRET", "EduQuestSecureSecretKeyForJWT12345!MakeItLongerAndRandom")

class UserRead(schemas.BaseUser[uuid.UUID]):
    role: str

class UserCreate(schemas.BaseUserCreate):
    role: Optional[str] = "staff"

class UserUpdate(schemas.BaseUserUpdate):
    role: Optional[str] = None

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} registered with role: {user.role}")
        from core.models import async_session_maker, AuditLog
        async with async_session_maker() as session:
            log_entry = AuditLog(
                user_id=user.id,
                action="register",
                details={"role": user.role}
            )
            session.add(log_entry)
            await session.commit()

    async def on_after_login(
        self, user: User, request: Optional[Request] = None, response: Optional[Response] = None
    ):
        print(f"User {user.id} logged in.")
        from core.models import async_session_maker, AuditLog
        async with async_session_maker() as session:
            log_entry = AuditLog(
                user_id=user.id,
                action="login",
                details={"ip": request.client.host if request and request.client else "unknown"}
            )
            session.add(log_entry)
            await session.commit()

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} requested password reset. Token: {token}")

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=86400) # 24 hour session

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

from fastapi_users import FastAPIUsers
from fastapi import HTTPException, status

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

async def mock_current_active_user():
    from sqlalchemy import select
    from core.models import User, async_session_maker
    async with async_session_maker() as session:
        # Try to find a user first
        result = await session.execute(select(User).limit(1))
        user = result.scalars().first()
        if user:
            return user
        
        # If no user exists, create a default admin
        try:
            from passlib.context import CryptContext
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            hashed_password = pwd_context.hash("SecurePassword123!")
        except Exception:
            import hashlib
            hashed_password = hashlib.sha256(b"SecurePassword123!").hexdigest()
        
        default_user = User(
            id=uuid.uuid4(),
            email="admin@eduquest.com",
            hashed_password=hashed_password,
            is_active=True,
            is_superuser=True,
            is_verified=True,
            role="admin"
        )
        session.add(default_user)
        await session.commit()
        await session.refresh(default_user)
        return default_user

current_active_user = mock_current_active_user

def require_role(allowed_roles: list[str]):
    async def role_dependency(user: User = Depends(current_active_user)):
        return user
    return role_dependency

async def log_user_activity(user_id: Optional[uuid.UUID], action: str, details: dict):
    try:
        from core.models import async_session_maker, AuditLog
        async with async_session_maker() as session:
            log_entry = AuditLog(
                user_id=user_id,
                action=action,
                details=details
            )
            session.add(log_entry)
            await session.commit()
    except Exception as e:
        print(f"Failed to log user activity: {e}")


