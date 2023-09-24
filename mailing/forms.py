from mailing.models import Client, Message, MailingSettings, MailingAttempt
from django import forms


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ('user',)


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
        exclude = ('user',)


class MailingSettingsForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingSettings
        fields = '__all__'
        exclude = ('user',)
        widgets = {
            'message': forms.Select,
            'client': forms.CheckboxSelectMultiple,
        }


class UserMailingSettingsForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingSettings
        fields = ['status', ]


class MailingAttemptForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingAttempt
        fields = '__all__'
