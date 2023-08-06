from django.db import models
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder


class Callbacks(models.Model):
    bank_id = models.IntegerField()
    type_code = models.IntegerField()
    reference = models.CharField(max_length=100, unique=True)
    callback = models.TextField()
    request = models.JSONField(default=dict)
    response = models.JSONField(default=dict)
    request_time = models.DateTimeField(default=timezone.now)
    response_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.reference

    def __repr__(self):
        return f'Callbacks(reference="{self.reference}",callback="{self.callback}", request={self.request}, response={self.response})'


class RequestLogs(models.Model):
    ip = models.CharField(max_length=50)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=100)
    content_type = models.CharField(max_length=50)
    content_params = models.JSONField(default=dict)
    body = models.JSONField(default=dict)
    headers = models.JSONField(default=dict)
    user = models.CharField(max_length=100)
    error=models.TextField(default=None,null=True)
    log_time = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = "Request Log"
        verbose_name_plural = "Request Logs"

    def __str__(self):
        return f'{self.log_time.strftime("%d %B %Y - %H:%M:%S")} {self.ip} {self.method} {self.path}'

    def __repr__(self):
        return f'RequestLogs(ip="{self.ip}", method="{self.method}", path="{self.path}", content_type="{self.content_type}", content_params="{self.content_params}", body="{self.body}", headers="{self.headers}", user="{self.user}")'


class ResponseLogs(models.Model):
    ip = models.CharField(max_length=50,default=None,null=True)
    headers = models.JSONField(default=dict)
    content = models.JSONField(default=dict)
    log_time = models.DateTimeField(default=timezone.now)
    error=models.TextField(default=None,null=True)

    def __str__(self):
        return f'{self.log_time.strftime("%d %B %Y - %H:%M:%S")} {self.ip}'

    def __repr__(self):
        return f'ResponseLogs(headers="{self.headers}", content="{self.content}")'
    
    class Meta:
        verbose_name = "Response Log"
        verbose_name_plural = "Response Logs"