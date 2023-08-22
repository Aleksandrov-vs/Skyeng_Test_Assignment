import time

from .models import ScriptCheck, CheckReport, ScriptCheckStatus
from .reports.services import ReportService
from .reports.linters import MyPyLinter, Flake8Linter
from users.tasks import send_email_with_report

from celery import shared_task


@shared_task
def create_and_send_report(script_check_id):
    time.sleep(5)
    try:
        script_check = ScriptCheck.objects.get(id=script_check_id)
    except ScriptCheck.DoesNotExist:
        return f" ScriptCheck with id {script_check_id} not found."
    else:
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
            send_email_with_report.apply_async(args=[script_check_id])
            return f"Отчеты успешно сохранены"

