from django.urls import path
from code_monitoring.views import ScriptView, ScriptCheckView, PatchScriptView, \
    DeleteScriptView

urlpatterns = [
    path('', ScriptView.as_view(), name='home'),
    path(
        'script/<uuid:script_id>/patch',
        PatchScriptView.as_view(),
        name='patch_script'
    ),path(
        'script/<uuid:script_id>/delete',
        DeleteScriptView.as_view(),
        name='delete_script'
    ),
    path(
        'script/detail/<uuid:script_id>/',
        ScriptCheckView.as_view(),
        name='script_check_detail'
    ),
]
