from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'event_date', 'max_guests', 'created_at')
    list_filter = ('event_date',)
    search_fields = ('title', 'location')