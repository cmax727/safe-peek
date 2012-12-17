from celery.task import task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail import send_mail

import celery


@celery.task
def notify():
    """
    Send an admin notification email when something happens
    """
    send_mail('pakai gmail', 'Email been verified', 'benhardrisando@gmail.com', ['flow_magnetic@yahoo.co.id'])
    return 'tessssssss ***********************'
