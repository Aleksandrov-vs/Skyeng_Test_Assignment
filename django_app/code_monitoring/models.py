import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from users.models import User


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ScriptStatus(models.TextChoices):
    DELETE = 'deleted', _('Deleted')
    NEW = 'new', _('New')
    UPDATE = 'updated', _('Updated')


class Script(UUIDMixin, TimeStampedMixin):
    user = models.ForeignKey(
        User,
        models.DO_NOTHING,
        blank=True,
    )
    script_name = models.TextField(_('script_name'), null=False)
    script_state = models.TextField(
        _('script_status'),
        choices=ScriptStatus.choices,
        default=ScriptStatus.NEW,
        null=False
    )
    file_path = models.FileField(
        _('file_path'),
        upload_to='scripts/',
        null=False,
        validators=[FileExtensionValidator(allowed_extensions=['py', ])]
    )

    def __str__(self):
        return self.file_path.name


class ScriptCheckStatus(models.TextChoices):
    PENDING = 'pending', _('Pending')
    CHECKED = 'checked', _('Checked')


class ScriptCheck(UUIDMixin, TimeStampedMixin):
    script = models.ForeignKey(Script, on_delete=models.CASCADE)
    script_check_status = models.TextField(
        _('script_check_status'),
        choices=ScriptCheckStatus.choices,
        default=ScriptCheckStatus.PENDING,
        null=False
    )
    is_email_send = models.BooleanField(
        _('email_is_send'),
        default=False,
        null=False
    )


class CheckReport(UUIDMixin, TimeStampedMixin):
    checking_script = models.ForeignKey(
        ScriptCheck,
        on_delete=models.CASCADE,
        related_name='checking_scripts'
    )
    linter_name = models.TextField(_('title'), null=False)
    file_path = models.FileField(
        _('file_path'),
        upload_to='check_reports/',
        null=False,
        validators=[FileExtensionValidator(allowed_extensions=['html', ])]
    )
