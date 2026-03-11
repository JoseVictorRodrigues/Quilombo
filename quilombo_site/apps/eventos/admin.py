from django.contrib import admin
from .models import Evento


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data', 'hora', 'local', 'google_event_id')
    list_filter = ('data',)
    search_fields = ('titulo', 'descricao', 'local')
    date_hierarchy = 'data'
    readonly_fields = ('google_event_id',)
