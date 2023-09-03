from django import forms
from mailing.models import MailingSettings, MailingAttempt


class MailingSettingsForm(forms.ModelForm):
    class Meta:
        model = MailingSettings
        fields = '__all__'


class MailingAttemptForm(forms.ModelForm):
    class Meta:
        model = MailingAttempt
        fields = '__all__'
