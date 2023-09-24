from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Title')
    text = models.TextField(verbose_name='Text')
    picture = models.ImageField(upload_to='blog/', verbose_name='Picture')

    count_of_views = models.IntegerField(default=0, verbose_name='Count of views')
    published_date = models.DateTimeField(verbose_name='Published time', **NULLABLE)

    def __str__(self):
        return (f'Title: {self.title}'
                f'Published time: {self.published_date}'
                f'Count of views: {self.count_of_views}')

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
