from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
# from djnago.utils import  timezone
# from datetime import datetime
# from config.celery import app
# from celery import shared_task


User = get_user_model()

# @app.task
def send_activation_code(email, activation_code):
    activation_link = f'http://127.0.0.1:8000/api/account/activate/{activation_code}/'
    html_message = render_to_string(
        'account/code_mail.html',
        {'activation_link': activation_link}
        )
    send_mail(
        'Активируйте ваш аккаунт!',
        '',
        settings.EMAIL_HOST_USER,
        [email],
        html_message=html_message,
        fail_silently=False
    )
