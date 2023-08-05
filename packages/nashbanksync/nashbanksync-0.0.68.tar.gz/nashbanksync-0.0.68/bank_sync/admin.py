from django.contrib import admin
from bank_sync.models import Callbacks, RequestLogs, ResponseLogs

# Register your models here.

admin.site.register(Callbacks)
admin.site.register(RequestLogs)
admin.site.register(ResponseLogs)
