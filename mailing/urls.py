from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, MessageListView, \
    MessageCreateView, MessageUpdateView, MessageDeleteView, MailingSettingsListView, MailingSettingsCreateView, \
    MailingSettingsUpdateView, MailingSettingsDeleteView, UserMailingSettingsListView, StatusMailingSettingsUpdateView, \
    MailingAttemptList

app_name = MailingConfig.name

urlpatterns = [

    path('clientlist/', ClientListView.as_view(), name='client_list'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

    path('messagelist/', MessageListView.as_view(), name='message_list'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),

    path('mailingsettings/', MailingSettingsListView.as_view(), name='mailing_settings_list'),
    path('mailingsettings/create/', MailingSettingsCreateView.as_view(), name='mailing_settings_create'),
    path('mailingsettings/update/<int:pk>', MailingSettingsUpdateView.as_view(), name='mailing_settings_update'),
    path('mailingsettings/delete/<int:pk>/', MailingSettingsDeleteView.as_view(), name='mailing_settings_delete'),

    path('mailing_attempts_list/', MailingAttemptList.as_view(), name='mailing_attempts_list'),

    path('users_mailing_settings_list/', UserMailingSettingsListView.as_view(), name='users_mailing_settings_list'),
    path('users_mailing_settings_status_update/<int:pk>/', StatusMailingSettingsUpdateView.as_view(),
         name='users_mailing_settings_status_update'),

]
