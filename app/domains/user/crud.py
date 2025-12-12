from sqlalchemy.orm import Session
from datetime import datetime
from app.domains.user.models import (
    User, 
    UserProfile, 
    UserBusiness, 
    UserBankInfo, 
    UserDocument,
    UserPushSetting, 
    RefreshToken,
    UploadHistory
)
from app.domains.user.schemas import (
    UserSignup,
    UserBankInfoSchema
)
from app.utils.file import get_file_hash, validate_file, save_file

class UserCRUD:
    # ----------------------
    # User 생성
    # ----------------------
    @staticmethod
    def create_user(db: Session, signup: UserSignup, hashed_pw: str):
        user = User(
            email=signup.email,
            password=hashed_pw,
            name=signup.name,
        )
        db.add(user)
        db.flush()

        return user

    # ----------------------
    # UserProfile 생성
    # ----------------------
    @staticmethod
    def create_user_profile(db: Session, user_id: int, signup: UserSignup):
        profile = UserProfile(
            user_id=user_id,
            phone=signup.phone,
            birthday=signup.birthday,
            gender=signup.gender,
            address=signup.address,
            address_detail=signup.address_detail,
            zipcode=signup.zipcode,
        )
        db.add(profile)
        return profile

    # ----------------------
    # UserBusiness 생성
    # ----------------------
    @staticmethod
    def create_user_business(db: Session, user_id: int, signup: UserSignup):
        if not signup.business_name:
            return None

        business = UserBusiness(
            user_id=user_id,
            business_name=signup.business_name,
            business_number=signup.business_number,
            ceo_name=signup.ceo_name,
            business_type=signup.business_type,
            business_item=signup.business_item,
            tel=signup.tel,
            address=signup.business_address,
            address_detail=signup.business_address_detail,
            zipcode=signup.business_zipcode,
        )
        db.add(business)
        return business

    # ----------------------
    # UserBankInfo 생성
    # ----------------------
    @staticmethod
    def create_user_bank_info(db: Session, user_id: int, bank_info: UserBankInfoSchema):
        if not bank_info:
            return None

        bank = UserBankInfo(
            user_id=user_id,
            bank_name=bank_info.bank_name,
            account_number=bank_info.account_number,
            holder_name=bank_info.holder_name,
        )
        db.add(bank)
        return bank

    # ----------------------
    # UserDocument 생성 (여러 개)
    # ----------------------
    @staticmethod
    def create_user_documents(db: Session, user_id: int, doc_type, upload_file):
        content = upload_file.file.read()

        try:
            # 1. 파일 검증
            ext = validate_file(upload_file, content)

            # 2. 파일 해시 생성
            file_hash = get_file_hash(content)

            # 3. 이미 동일한 파일 존재하면 중복 저장 방지
            exist = db.query(UserDocument).filter_by(file_hash=file_hash).first()
            if exist:
                raise ValueError("이미 업로드된 동일한 파일입니다.")

            # 4. 실제 파일 저장
            file_path = save_file(content, file_hash, ext)

            # 5. DB row 생성
            document = UserDocument(
                user_id=user_id,
                doc_type=doc_type,
                file_name=upload_file.filename,
                file_url=file_path,
                file_hash=file_hash,
                file_size=len(content),
                ext=ext,
            )
            db.add(document)

            # 6. 업로드 이력 저장
            history = UploadHistory(
                file_name=upload_file.filename,
                file_hash=file_hash,
                status="success",
            )
            db.add(history)

            return document

        except Exception as e:
            db.add(UploadHistory(
                file_name=upload_file.filename,
                file_hash="unknown",
                status="failed",
                reason=str(e)
            ))
            raise
    
    @staticmethod
    def get_by_userID(db: Session, user_id: str):
        return db.query(User).filter(User.user_id == user_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(UserProfile).filter(UserProfile.email == email).first()

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