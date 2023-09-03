from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """Клиент сервиса:"""
    email = models.EmailField(verbose_name='Контактный email')
    first_name = models.CharField(max_length=50, verbose_name='Имя', **NULLABLE)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', **NULLABLE)
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}: {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    """Сообщение для рассылки"""

    theme = models.CharField(max_length=100, **NULLABLE, verbose_name='Тема сообщения')
    message = models.TextField(**NULLABLE, verbose_name='Сообщение')

    def __str__(self):
        return f'{self.theme}: {self.message}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class MailingSettings(models.Model):
    """Рассылка (настройки)"""
    PERIOD_DAILY = 'daily'
    PERIOD_WEEKLY = 'weekly'
    PERIOD_MONTHLY = 'monthly'

    PERIODS = (
        (PERIOD_DAILY, 'Ежедневная'),
        (PERIOD_WEEKLY, 'Раз в неделю'),
        (PERIOD_MONTHLY, 'Раз в месяц'),
    )

    STATUS_CREATED = 'created'
    STATUS_STARTED = 'started'
    STATUS_DONE = 'done'
    STATUSES = (
        (STATUS_CREATED, 'Создана'),
        (STATUS_STARTED, 'Запущена'),
        (STATUS_DONE, 'Завершена'),
    )
    time = models.TimeField(verbose_name='Время')
    period = models.CharField(max_length=25, choices=PERIODS, default=PERIOD_DAILY, verbose_name='Период')
    status = models.CharField(max_length=25, choices=STATUSES, default=STATUS_CREATED, verbose_name='Статус')

    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение', **NULLABLE)

    def __str__(self):
        return f'{self.time}, {self.period}'

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'


class MailingClient(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    settings = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='Настройка')

    def __str__(self):
        return f'{self.client} / {self.settings}'

    class Meta:
        verbose_name = 'Клиент рассылки'
        verbose_name_plural = 'Клиенты рассылки'


class MailingAttempt(models.Model):
    """Попытка рассылки"""

    STATUS_OK = 'ok'
    STATUS_ERROR = 'error'
    STATUSES = (
        (STATUS_OK, 'Успешно'),
        (STATUS_ERROR, 'Ошибка'),
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    message = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='Настройки')

    attempt_date = models.DateTimeField(auto_now_add=True, **NULLABLE, verbose_name='Дата и время последней попытки')
    status = models.CharField(max_length=25, choices=STATUSES, default=STATUS_OK, verbose_name='Статус попытки')
    server_response = models.TextField(**NULLABLE, verbose_name='Ответ почтового сервера')

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
