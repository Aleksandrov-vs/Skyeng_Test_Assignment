
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, View

from .decorators.access_decorators import user_has_script_access, \
    user_has_script_check_access
from .models import Script, ScriptCheck, ScriptStatus, ScriptCheckStatus
from .forms import UploadScriptForm, PatchScriptForm
from .tasks import create_and_send_report


@method_decorator([login_required(), user_has_script_access], name='dispatch')
class DeleteScriptView(View):
    success_url = 'home'
    template_name = 'home.html'

    def post(self, request, *args, **kwargs):
        script_id = self.kwargs['script_id']
        script = Script.objects.get(id=script_id)
        script.script_state = ScriptStatus.DELETE
        script.save()
        return HttpResponseRedirect(
            reverse(self.success_url)
        )


@method_decorator(login_required(), name='dispatch')
class ScriptView(ListView):
    template_name = 'home.html'
    model = Script
    context_object_name = 'upload_script_list'
    success_url = 'home'

    def get_queryset(self):
        current_user = self.request.user
        return Script.objects.filter(
            user=current_user
        ).exclude(
            script_state=ScriptStatus.DELETE
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upload_script_form'] = UploadScriptForm()
        return context

    def post(self, request, *args, **kwargs):
        form = UploadScriptForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = self.request.user
            form.instance.user = current_user
            form.instance.script_name = str(form.instance.file_path)
            script = form.save()
            script_check = ScriptCheck(script=script)
            script_check.save()

            create_and_send_report.apply_async(args=[script_check.id])

            return HttpResponseRedirect(reverse(self.success_url))
        else:
            return render(request, self.template_name, {
                'upload_script_form': form,
                self.context_object_name: self.get_queryset()
            })


@method_decorator([login_required(), user_has_script_check_access], name='dispatch')
class ScriptCheckView(ListView):
    template_name = 'script_check_detail.html'
    model = ScriptCheck
    context_object_name = 'checking_scripts_list'
    success_url = 'script_check_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patch_script_form'] = PatchScriptForm()
        return context

    def get_queryset(self):
        script_id = self.kwargs['script_id']
        script_checks_with_reports = ScriptCheck.objects.filter(
            script_id=script_id
        ).prefetch_related('check_report')
        return script_checks_with_reports

    def post(self, request, *args, **kwargs):
        script_id = self.kwargs['script_id']
        form = PatchScriptForm(request.POST, request.FILES)

        script = Script.objects.get(id=script_id)
        script_checks = ScriptCheck.objects.filter(script=script)

        if script_checks.filter(
                script_check_status=ScriptCheckStatus.PENDING).exists():
            form.add_error(None, "Дождитесь окончания предыдущей проверки")

        if form.is_valid():
            new_file = request.FILES.get('file_path')
            if new_file:
                script.file_path = new_file

            script.script_state = ScriptStatus.UPDATE
            script.save()

            script_check = ScriptCheck(script=script)
            script_check.save()

            create_and_send_report.apply_async(args=[script_check.id])

            return HttpResponseRedirect(
                reverse(self.success_url, args=[script_id])
            )
        else:
            return render(
                request,
                self.template_name,
                context={
                    'patch_script_form': form,
                    self.context_object_name:  self.get_queryset()
                }
            )


