import random

from django.views.generic import ListView, DetailView

from blog.models import Blog
from mailing.models import MailingSettings, Client

from django.core.cache import cache
from django.conf import settings
from .models import Blog


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if settings.CACHE_ENABLED:
            total_mailings = cache.get('total_mailings')
            active_mailings = cache.get('active_mailings')
            unique_clients = cache.get('unique_clients')

            if total_mailings is None:
                total_mailings = MailingSettings.objects.count()
                cache.set('total_mailings', total_mailings)

            if active_mailings is None:
                active_mailings = MailingSettings.objects.filter(status=MailingSettings.STATUS_STARTED).count()
                cache.set('active_mailings', active_mailings)

            if unique_clients is None:
                unique_clients = Client.objects.count()
                cache.set('unique_clients', unique_clients)
        else:
            total_mailings = MailingSettings.objects.count()
            active_mailings = MailingSettings.objects.filter(status=MailingSettings.STATUS_STARTED).count()
            unique_clients = Client.objects.count()

        context['total_mailings'] = total_mailings
        context['active_mailings'] = active_mailings
        context['unique_clients'] = unique_clients
        return context

    def get_queryset(self):
        all_blogs = Blog.objects.all()

        if settings.CACHE_ENABLED:
            cached_blogs = cache.get('random_blogs')
            if cached_blogs is None:
                cached_blogs = random.sample(list(all_blogs), 3)
                cache.set('random_blogs', cached_blogs)
            return cached_blogs
        else:
            return random.sample(list(all_blogs), 3)


class BlogDetailView(DetailView):
    model = Blog

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(pk=self.kwargs.get('pk', None))
        return queryset

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count_of_views += 1
        self.object.save()
        return self.object
