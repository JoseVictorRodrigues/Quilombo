import logging
from datetime import date
from django.shortcuts import render, get_object_or_404
from django.core.cache import cache
from apps.core.models import ConfiguracaoSite
from .models import Evento
from .sync_calendar import sincronizar_calendario

logger = logging.getLogger(__name__)

# Chave de cache para evitar sincronizações repetidas
_SYNC_CACHE_KEY = 'gcal_last_sync'
_SYNC_CACHE_TIMEOUT = 30 * 60  # 30 minutos

# URL padrão do feed ICS (usado se ConfiguracaoSite não tiver link configurado)
_DEFAULT_ICS_URL = 'https://calendar.google.com/calendar/ical/quilomboaraucaria%40gmail.com/public/basic.ics'


def agenda(request):
    # Sincronizar com Google Calendar (com cache de 30 min)
    if not cache.get(_SYNC_CACHE_KEY):
        config = ConfiguracaoSite.get()
        url_ics = config.google_calendar_link or _DEFAULT_ICS_URL
        try:
            stats = sincronizar_calendario(url_ics)
            logger.info('Sync automático: %s', stats)
        except Exception as e:
            logger.error('Erro na sincronização automática: %s', e)
        cache.set(_SYNC_CACHE_KEY, True, _SYNC_CACHE_TIMEOUT)

    proximos_eventos = Evento.objects.filter(data__gte=date.today())
    return render(request, 'eventos/agenda.html', {
        'proximos_eventos': proximos_eventos,
    })


def detalhe_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    return render(request, 'eventos/detalhe.html', {'evento': evento})
