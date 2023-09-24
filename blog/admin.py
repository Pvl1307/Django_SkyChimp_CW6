from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class WeBlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'count_of_views')
