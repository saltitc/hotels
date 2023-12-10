# from pydantic import EmailStr
# from app.config import settings
from app.tasks.celery import celery
from PIL import Image
from pathlib import Path
# import smtplib

# from app.tasks.email_templates import create_booking_confirmation_template


@celery.task
def process_pic(path: str):
    img_path = Path(path)
    img = Image.open(img_path)
    img_resized_1 = img.resize((1000, 500))
    img_resized_2 = img.resize((200, 100))
    img_resized_1.save(f"app/static/images/resized_1000_500_{img_path.name}")
    img_resized_2.save(f"app/static/images/resized_200_100_{img_path.name}")


# @celery.task
# def send_booking_confirmation_email(booking: dict, email_to: EmailStr):
#     email_to_mock = settings.SMTP_USER
#     msg_content = create_booking_confirmation_template(booking, email_to_mock)

#     with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
#         server.login(settings.SMTP_USER, settings.SMTP_PASS)
#         server.send_message(msg_content)
