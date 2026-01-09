import json
import httpx
from sqlalchemy.orm import Session
from app.core.exceptions import AppException
from app.core.config import settings
from ..crud import create_send_log


basic_send_url = "https://kakaoapi.aligo.in/akv10/alimtalk/send/"


import logging
logger = logging.getLogger(__name__)


class Kakao:
    @staticmethod
    async def send(
        db: Session,
        user_id: int,
        phone: str,
        title: str,
        message: str
    ):
        try:
            # -------------------------------------------------------------------------------------------------
            # BUTTON
            #
            # name: 버튼명, 
            # linkType: 버튼 링크타입(DS:배송조회, WL:웹링크, AL:앱링크, BK:봇키워드, MD:메시지전달),
            # linkTypeName : 버튼 링크 타입네임, ( 배송조회, 웹링크, 앱링크, 봇키워드, 메시지전달 중에서 1개) 
            # linkM: 모바일 웹링크주소(WL일 때 필수), linkP: PC웹링크 주소(WL일 때 필수),
            # linkI: IOS앱링크 주소(AL일 때 필수), linkA: Android앱링크 주소(AL일 때 필수)
            button_info = {
                "button": [
                    {
                        "name": "채널추가",
                        "linkType": "AC",
                        "linkTypeName": "채널추가",
                    },
                    {
                        "name": "확인하러가기",
                        "linkType": "WL",
                        "linkTypeName": "웹링크",
                        "linkMo": "https://a.co.kr",
                    },
                ]
            }

            button_info = json.dumps(button_info, ensure_ascii=False)

            kakao_data={
                'apikey': settings.SMS_SEND_KEY,
                'userid': settings.SMS_SEND_ID,
                'senderkey': 'dbc40f19cf29c36c794568f6c7c9a952ced08206',
                'tpl_code': 'TZ_3940',
                'sender' : settings.SMS_SEND_NUMBER,
                'receiver_1': phone,
                'subject_1': title,
                'message_1': message,
                'button_1': button_info,
            }
            
            async with httpx.AsyncClient(verify=False) as client:
                response = await client.post(
                    basic_send_url,
                    data=kakao_data
                )

            body = response.json()
            info = body.get("info", {})

            create_send_log(
                db,
                user_id=user_id,
                phone=phone,
                title=title,
                message=message,
                result_message=body.get("message"),
                result_code=body.get("code"),
                msg_id=info.get("mid"),
                error_cnt=info.get("fcnt"),
                success_cnt=info.get("scnt"),
                msg_type="kakao",
            )

            db.commit()

            return {
                "result_code": body.get("result_code"),
                "message": body.get("message"),
                "msg_id": body.get("msg_id"),
            }       
         
        except Exception as e:
            db.rollback()
            logger.exception("알림톡 발송 실패: %s", e)
            raise AppException("알림톡 발송에 실패하였습니다.", 500)
