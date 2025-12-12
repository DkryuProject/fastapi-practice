from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.domains.user.crud import UserCRUD
from app.core.security import hash_password,verify_password
from app.core.jwt import decode_token, create_access_token, create_refresh_token
from app.domains.user.schemas import UserSignup
from app.core.exceptions import AppException
from fastapi import UploadFile

import logging
logger = logging.getLogger(__name__)


class UserService:
    @staticmethod
    def signup(db: Session, signup: UserSignup, files: list[UploadFile]):
        try:
            # UserID 중복 체크
            if UserCRUD.get_by_userID(db, signup.user_id):
                raise AppException("이미 가입된 ID입니다.", 400)

            if UserCRUD.get_by_email(db, signup.profile.email):
                raise AppException("이미 가입된 이메일입니다.", 400)
            
            # 비밀번호 해시
            hashed_pw = hash_password(signup.password)

            # 유저 생성
            user = UserCRUD.create_user(db, signup, hashed_pw)

            # 프로필 생성
            UserCRUD.create_user_profile(db, user.id, signup)

            # 사업자 정보 생성
            UserCRUD.create_user_business(db, user.id, signup)

            # 은행 정보 생성
            if signup.bank_info:
                UserCRUD.create_user_bank_info(db, user.id, signup.bank_info)

            # 문서 정보 생성(중요 부분)
            if signup.documents and files:
                if len(signup.documents) != len(files):
                    raise AppException("문서 정보와 파일 개수가 일치하지 않습니다.", 400)

            for idx, meta in enumerate(signup.documents):
                file: UploadFile = files[idx]
                UserCRUD.create_user_documents(db, user.id, meta.doc_type, file)

            # 모든 insert가 문제 없으면 commit
            db.commit()
            db.refresh(user)

            return {"message": "회원가입 성공", "user_id": user.id}

        except Exception as e:
            db.rollback()
            logger.exception("회원가입 실패: ", e)
            raise AppException("회원가입에 실패하였습니다.", 500)

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
