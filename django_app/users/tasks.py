import logging

from celery import shared_task

from config import settings
from code_monitoring.models import ScriptCheck

from django.core.mail import send_mail


@shared_task
def send_email_with_report(script_check_id):
    script_check = ScriptCheck.objects.select_related(
        "script", "script__user"
    ).prefetch_related('check_report').get(
        id=script_check_id
    )

    user = script_check.script.user
    subject = 'Проверка кода'
    reports = script_check.check_report.all()
    message = 'Ура ваш код проверен.\n Линетры:'
    for report in reports:
        message += f'{report.linter_name} '
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email, ]
        )
        print(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email, ]
        )
        return f'Cообщение о проверке {script_check_id} отправлено.'
    except Exception as e:
        return f'Ошибка при отправки email с отчетом {str(e)}'
