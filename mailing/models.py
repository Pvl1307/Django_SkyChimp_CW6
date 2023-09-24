from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """Клиент сервиса:"""
    email = models.EmailField(verbose_name='Email')
    first_name = models.CharField(max_length=50, verbose_name='Name', **NULLABLE)
    last_name = models.CharField(max_length=50, verbose_name='Surname', **NULLABLE)
    comment = models.TextField(verbose_name='Comment', **NULLABLE)

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')

    def __str__(self):
        return f'{self.first_name} {self.last_name}: {self.email}'

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class Message(models.Model):
    """Сообщение для рассылки"""

    theme = models.CharField(max_length=100, **NULLABLE, verbose_name='Message theme')
    message = models.TextField(**NULLABLE, verbose_name='Message text')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')

    def __str__(self):
        return f'{self.theme}: {self.message}'

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'


class MailingSettings(models.Model):
    """Рассылка (настройки)"""
    PERIOD_DAILY = 'daily'
    PERIOD_WEEKLY = 'weekly'
    PERIOD_MONTHLY = 'monthly'

    PERIODS = (
        (PERIOD_DAILY, 'Daily'),
        (PERIOD_WEEKLY, 'Weekly'),
        (PERIOD_MONTHLY, 'Monthly'),
    )

    STATUS_CREATED = 'created'
    STATUS_STARTED = 'started'
    STATUS_DONE = 'done'
    STATUSES = (
        (STATUS_CREATED, 'Created'),
        (STATUS_STARTED, 'Started'),
        (STATUS_DONE, 'Done'),
    )
    time = models.TimeField(verbose_name='Time')
    period = models.CharField(max_length=25, choices=PERIODS, default=PERIOD_DAILY, verbose_name='Period')
    status = models.CharField(max_length=25, choices=STATUSES, default=STATUS_CREATED, verbose_name='Status')

    client = models.ManyToManyField(Client, verbose_name='Client')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Message', **NULLABLE)

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')

    def __str__(self):
        clients_list = "\n".join([str(client) for client in self.client.all()])
        return (
            f'Time: {self.time}\n'
            f'Clients:{clients_list}\n'
            f'Message: {self.message}'
        )

    class Meta:
        verbose_name = 'Mailing setting'
        verbose_name_plural = 'Mailing settings'

        permissions = [
            ('set_status', 'Can change status of mailing')
        ]


class MailingAttempt(models.Model):
    """Попытка рассылки"""

    STATUS_OK = 'OK'
    STATUS_ERROR = 'ERROR'
    STATUSES = (
        (STATUS_OK, 'OK'),
        (STATUS_ERROR, 'ERROR'),
    )

    settings = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='Mailing settings')

    attempt_date = models.DateTimeField(auto_now_add=True, **NULLABLE, verbose_name='Дата и время последней попытки')
    status = models.CharField(choices=STATUSES, default=STATUS_OK, verbose_name='Attempt status')
    server_response = models.TextField(**NULLABLE, verbose_name='Server response')

    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'
