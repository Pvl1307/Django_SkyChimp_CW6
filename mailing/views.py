from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.forms import CheckboxSelectMultiple
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from mailing.models import Client, Message, MailingSettings, MailingAttempt
from mailing.forms import MailingSettingsForm, ClientForm, MessageForm, UserMailingSettingsForm


#####################################################CLIENTS############################################################
class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'mailing/client_list.html'

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            user=self.request.user
        )
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        return queryset


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mailing:client_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')


########################################################MESSAGE#########################################################

class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailing/message_list.html'

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            user=self.request.user
        )
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        return queryset


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mailing:message_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')


####################################MAILING_SETTINGS####################################################################
class MailingSettingsListView(LoginRequiredMixin, ListView):
    model = MailingSettings
    template_name = 'mailingsettings.html'

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            user=self.request.user
        )
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        return queryset


class MailingSettingsCreateView(LoginRequiredMixin, CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    template_name = 'mailing/mailingsettings_form.html'
    success_url = reverse_lazy('mailing:mailing_settings_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields['message'].queryset = Message.objects.filter(user=self.request.user)
        form.fields['client'].queryset = Client.objects.filter(user=self.request.user)

        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MailingSettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:mailing_settings_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_clients = self.object.client.values_list('pk', flat=True)
        context['selected_clients'] = selected_clients
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields['message'].queryset = Message.objects.filter(user=self.request.user)
        form.fields['client'].queryset = Client.objects.filter(user=self.request.user)

        form.fields['client'].widget = CheckboxSelectMultiple()
        return form


class MailingSettingsDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('mailing:mailing_settings_list')


class UserMailingSettingsListView(LoginRequiredMixin, ListView):
    model = MailingSettings
    template_name = 'mailing/usersmailingsettings_list.html'


class StatusMailingSettingsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = MailingSettings
    form_class = UserMailingSettingsForm
    success_url = reverse_lazy('mailing:users_mailing_settings_list')
    permission_required = 'mailing.set_status'


#####################################MAILINGATTEMPT#####################################################################

class MailingAttemptList(ListView):
    model = MailingAttempt
