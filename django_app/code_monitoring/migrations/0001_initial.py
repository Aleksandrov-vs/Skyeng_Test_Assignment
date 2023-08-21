# Generated by Django 4.2.4 on 2023-08-21 05:18

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Script',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('script_name', models.TextField(verbose_name='script_name')),
                ('script_state', models.TextField(choices=[('deleted', 'Deleted'), ('new', 'New'), ('checked', 'Checked'), ('updated', 'Updated')], default='new', verbose_name='script_status')),
                ('file_path', models.FileField(upload_to='scripts/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['py'])], verbose_name='file_path')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ScriptCheck',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('script_check_status', models.TextField(choices=[('pending', 'Pending'), ('checked', 'Checked')], default='pending', verbose_name='script_check_status')),
                ('is_email_send', models.BooleanField(default=False, verbose_name='email_is_send')),
                ('script', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='code_monitoring.script')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CheckReport',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('linter_name', models.TextField(verbose_name='title')),
                ('file_path', models.FileField(upload_to='check_reports/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['html'])], verbose_name='file_path')),
                ('checking_script', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='code_monitoring.scriptcheck')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
