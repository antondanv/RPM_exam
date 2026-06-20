from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'phone', 'registration_date', 'created_at')
    list_filter = ('registration_date',)
    search_fields = ('full_name', 'email', 'phone')
