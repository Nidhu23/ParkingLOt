# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
import time
from django.core.mail import send_mail
from ParkingLotSystem import settings


@shared_task
def send_notification(mail_id, user):
    subject = 'Welcome to Sample Parking Lot'
    message = 'Hi, ' + user + '! thank you for registering with us.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [
        mail_id,
    ]
    send_mail(subject, message, from_email, recipient_list)
