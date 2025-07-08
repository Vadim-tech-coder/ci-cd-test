"""
В этом файле будут Celery-задачи
"""
from celery.schedules import crontab

from image import blur_image
from celery import Celery

from app import email_addresses
from mail import send_email

celery_ap = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)
celery_ap.conf.timezone = 'Asia/Yekaterinburg'
celery_ap.conf.beat_schedule = {
    'send-emails-every-tuesday-1225': {
        'task': 'sending_emails',
        'schedule': crontab(hour=12, minute=25, day_of_week='tue')
    },
}

@celery_ap.task
def process_images(image_path):
    blurred_image = blur_image(image_path)
    return blurred_image

# @celery_ap.on_after_configure.connect
# def configure_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(
#         crontab(hour='10', minute = '55', day_of_week = 'TUE'),
#         sending_emails.s(),
#         name = "Отправка писем"
#     )
#     return 'Successfully'




@celery_ap.task
def sending_emails():
    for email in email_addresses:
        send_email(
            order_id = 'Периодическая рассылка',
            receiver=email,
            filename="blurred_photos.zip"
        )
    return 'sending_mails'