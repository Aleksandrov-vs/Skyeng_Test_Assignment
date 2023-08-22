from django import forms
from .models import Script, ScriptCheck, ScriptCheckStatus


class UploadScriptForm(forms.ModelForm):
    class Meta:
        model = Script
        fields = ['file_path', ]


class PatchScriptForm(forms.ModelForm):
    file_path = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={'onchange': 'this.form.submit();'}
        )
    )

    class Meta:
        model = Script
        fields = ['file_path', ]
