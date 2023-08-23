import time

from .models import ScriptCheck, CheckReport, ScriptCheckStatus
from .reports.services import ReportService
from .reports.linters import MyPyLinter, Flake8Linter
from users.tasks import send_email_with_report

from celery import shared_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

@shared_task
def create_and_send_report():
    script_checks = ScriptCheck.objects.filter(
        script_check_status=ScriptCheckStatus.PENDING
    )
    if len(script_checks) == 0:
        return 'Нет новых отчетов для проверки'
    for script_check in script_checks:
        try:
            report_service = ReportService(
                linters_list=[MyPyLinter(), Flake8Linter()]
            )
            reports = report_service.create_reports(
                script_check.script.file_path.path
            )
            check_report_objects = [
                CheckReport(
                    script_check=script_check,
                    linter_name=report.linter_name,
                    report_text=report.report_text,

                ) for report in reports
            ]
            CheckReport.objects.bulk_create(check_report_objects)
        except Exception as e:
            script_check.script_check_status = ScriptCheckStatus.ERR
            script_check.save()
            return f"Ошибка при выполнении: {str(e)}"
        else:
            script_check.script_check_status = ScriptCheckStatus.CHECKED
            script_check.save()
            send_email_with_report.apply_async(args=[script_check.id])
            return f"Отчеты успешно сохранены"
