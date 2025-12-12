from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.domains.user.crud import UserCRUD
from app.core.security import hash_password,verify_password
from app.core.jwt import decode_token, create_access_token, create_refresh_token
from app.domains.user.schemas import UserSignup
from app.core.exceptions import AppException


class UserService:
    @staticmethod
    def signup(db: Session, payload: UserSignup):
        # 이메일 중복 체크
        if UserCRUD.get_by_email(db, payload.email):
            raise AppException("이미 가입된 이메일입니다.", 500)

        # 1) 유저 생성
        user = UserCRUD.create_user(
            db,
            email=payload.email,
            password=hash_password(payload.password),
            name=payload.name,
        )

        # 2) 프로필 저장
        profile_data = {
            "phone": payload.phone,
            "birthday": payload.birthday,
            "gender": payload.gender,
            "address": payload.address,
            "address_detail": payload.address_detail,
            "zipcode": payload.zipcode
        }
        UserCRUD.create_profile(db, user.id, profile_data)

        # 3) 사업자 정보 저장
        business_data = {
            "business_name": payload.business_name,
            "business_number": payload.business_number,
            "ceo_name": payload.ceo_name,
            "business_type": payload.business_type,
            "business_item": payload.business_item,
            "tel": payload.tel,
            "address": payload.business_address,
            "address_detail": payload.business_address_detail,
            "zipcode": payload.business_zipcode
        }
        UserCRUD.create_business(db, user.id, business_data)

        # 4) 푸시 설정 초기화
        UserCRUD.create_push_setting(db, user.id)

        return user

    @staticmethod
    def login(db: Session, email: str, password: str):
        user = UserCRUD.get_by_email(db, email)
        if not user:
            raise Exception("존재하지 않는 이메일입니다.")

        if not verify_password(password, user.password):
            raise Exception("비밀번호가 일치하지 않습니다.")

        # 리프레시 토큰 생성 및 저장
        refresh_token, expires = create_refresh_token(user.id)
        UserCRUD.add_refresh_token(db, user.id, refresh_token, expires)

        # 액세스 토큰 생성
        access_token = create_access_token(user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    @staticmethod
    def refresh_tokens(db, refresh_token: str):
        # 1. refresh token 해독 (서명 검증)
        try:
            payload = decode_token(refresh_token)
        except Exception:
            raise HTTPException(status_code=401, detail="유효하지 않은 Refresh Token 입니다.")

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Refresh Token 형식이 아닙니다.")

        user_id = int(payload.get("sub"))
        exp = payload.get("exp")

        # 2. DB에 존재하는지 확인
        stored = UserCRUD.get_refresh_token(db, refresh_token)
        if not stored:
            raise HTTPException(status_code=401, detail="등록되지 않은 Refresh Token 입니다.")

        # 3. 이미 폐기된 토큰인지 확인
        if stored.revoked:
            raise HTTPException(status_code=401, detail="이미 폐기된 Refresh Token 입니다.")

        # 4. 만료 여부 체크
        if datetime.utcnow().timestamp() > exp:
            stored.revoked = True
            db.commit()
            raise HTTPException(status_code=401, detail="Refresh Token 이 만료되었습니다.")

        # 5. 기존 Refresh Token 폐기
        stored.revoked = True
        db.commit()

        # 6. 새 Access Token & Refresh Token 발급
        new_access = create_access_token(user_id)
        new_refresh, expires = create_refresh_token(user_id)

        # DB에 새 토큰 저장
        UserCRUD.add_refresh_token(db, user_id, new_refresh, expires)

        return {
            "access_token": new_access,
            "refresh_token": new_refresh,
        }

    @staticmethod
    def logout(db, refresh_token: str):
        token = UserCRUD.get_refresh_token(db, refresh_token)
        if not token:
            raise HTTPException(status_code=400, detail="Refresh Token 이 존재하지 않습니다.")

        token.revoked = True
        db.commit()

        return True
