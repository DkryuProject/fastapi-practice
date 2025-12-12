from sqlalchemy.orm import Session
from datetime import datetime
from app.domains.user.models import (
    User, UserProfile, UserBusiness, UserPushSetting, RefreshToken
)


class UserCRUD:

    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create_user(db: Session, email: str, password: str, name: str | None):
        user = User(email=email, password=password, name=name)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def create_profile(db: Session, user_id: int, data: dict):
        profile = UserProfile(user_id=user_id, **data)
        db.add(profile)
        db.commit()
        return profile

    @staticmethod
    def create_business(db: Session, user_id: int, data: dict):
        business = UserBusiness(user_id=user_id, **data)
        db.add(business)
        db.commit()
        return business

    @staticmethod
    def create_push_setting(db: Session, user_id: int):
        setting = UserPushSetting(user_id=user_id)
        db.add(setting)
        db.commit()
        return setting

    @staticmethod
    def add_refresh_token(db: Session, user_id: int, token: str, expires_at: datetime):
        refresh = RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
        )
        db.add(refresh)
        db.commit()
        return refresh

    @staticmethod
    def get_refresh_token(db: Session, token: str) -> RefreshToken | None:
        return db.query(RefreshToken).filter(RefreshToken.token == token).first()

    @staticmethod
    def revoke_refresh_token(db: Session, refresh: RefreshToken):
        refresh.revoked = True
        db.commit()