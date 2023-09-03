from django.contrib import admin

from mailing.models import Client, Message, MailingSettings, MailingClient, MailingAttempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'comment')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('theme', 'message')


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('time', 'period', 'status', 'message')


@admin.register(MailingClient)
class MailingClientAdmin(admin.ModelAdmin):
    list_display = ('client', 'settings')


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('client', 'message', 'attempt_date', 'status', 'server_response')
