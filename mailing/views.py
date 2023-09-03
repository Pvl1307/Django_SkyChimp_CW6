from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from mailing.models import Client, Message, MailingSettings
from mailing.forms import MailingSettingsForm


def home(request):
    return render(request, 'mailing/base.html')


#####################################################CLIENTS############################################################
class ClientListView(ListView):
    model = Client
    template_name = 'mailing/client_list.html'


class ClientCreateView(CreateView):
    model = Client
    fields = '__all__'
    success_url = reverse_lazy('mailing:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    template_name = 'mailing/client_form.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('mailing:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')


########################################################MESSAGE#########################################################

class MessageListView(ListView):
    model = Message
    template_name = 'mailing/message_list.html'


class MessageCreateView(CreateView):
    model = Message
    fields = '__all__'
    success_url = reverse_lazy('mailing:message_list')


class MessageUpdateView(UpdateView):
    model = Message
    fields = '__all__'
    template_name = 'mailing/message_form.html'

    def get_success_url(self):
        return reverse('mailing:message_list')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')


####################################MAILINGSETTINGS#####################################################################
class MailingSettingsListView(ListView):
    model = MailingSettings
    template_name = 'mailingsettings.html'

    def get_period_display(self):
        return dict(self.PERIODS)[self.period]

    def get_status_display(self):
        return dict(self.STATUSES)[self.status]


class MailingSettingsCreateView(CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    template_name = 'mailing/mailingsettings_form.html'
    success_url = reverse_lazy('mailing:mailing_settings_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()

        context['time_field'] = form['time']
        context['period_field'] = form['period']
        context['status_field'] = form['status']
        context['message_field'] = form['message']
        return context


class MailingSettingsUpdateView(UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:mailing_settings_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.object
        return context

    def form_valid(self, form):
        form.instance.time = form.cleaned_data['time']
        return super().form_valid(form)


class MailingSettingsDeleteView(DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('mailing:mailing_settings_list')

#####################################MAILINGATTEMPT#####################################################################

