from django.contrib import admin
from .models import InstagramData


@admin.register(InstagramData)
class InstagramDataAdmin(admin.ModelAdmin) :
    list_display = ['username', 'sessionid', 'datetime_created']
    list_filter = ['datetime_created']
    ordering = ['datetime_created']
