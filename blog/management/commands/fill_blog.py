import json

from django.core.management import BaseCommand

from blog.models import Blog
from config.settings import BASE_DIR


class Command(BaseCommand):
    blog_file = f'{BASE_DIR}/blog_data.json'

    @staticmethod
    def json_read_blog():
        with open(Command.blog_file, 'r', encoding='utf-8') as f:
            blog_list = json.load(f)
        return blog_list

    def handle(self, *args, **options):
        Blog.objects.all().delete()
        blog_for_create = []

        for blog in Command.json_read_blog():
            blog_for_create.append(
                Blog(title=blog['fields']['title'],
                     text=blog['fields']['text'],
                     picture=blog['fields']['picture'],
                     count_of_views=blog['fields']['count_of_views'],
                     published_date=blog['fields']['published_date'])
            )

        Blog.objects.bulk_create(blog_for_create)
