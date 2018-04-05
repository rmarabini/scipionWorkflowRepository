from django.contrib import admin
from .models import WorkFlow, Category, Protocol
# Register your models here.

admin.site.register(WorkFlow)
admin.site.register(Category)
admin.site.register(Protocol)