"""
Serviço de sincronização do Google Calendar via ICS.
Importa eventos de um calendário público do Google para o modelo Evento.
"""
import logging
from datetime import date, datetime, time
from urllib.parse import urlparse

import requests
from icalendar import Calendar
from django.utils import timezone

from .models import Evento

logger = logging.getLogger(__name__)

# Timeout em segundos para requisição HTTP ao Google Calendar
_REQUEST_TIMEOUT = 15
# Tamanho máximo do arquivo ICS aceito (2 MB)
_MAX_ICS_SIZE = 2 * 1024 * 1024


def validar_url_ics(url):
    """Valida se a URL parece ser um link ICS seguro do Google Calendar."""
    if not url:
        return False
    parsed = urlparse(url)
    if parsed.scheme not in ('https',):
        return False
    dominios_permitidos = [
        'calendar.google.com',
    ]
    if parsed.hostname not in dominios_permitidos:
        return False
    return True


def sincronizar_calendario(url_ics):
    """
    Faz download do arquivo ICS e importa/atualiza eventos no banco.
    Retorna dict com estatísticas: criados, atualizados, erros.
    """
    stats = {'criados': 0, 'atualizados': 0, 'erros': 0, 'total_ics': 0}

    if not validar_url_ics(url_ics):
        logger.warning('URL ICS inválida ou não permitida: domínio não é calendar.google.com')
        stats['erros'] = 1
        return stats

    try:
        response = requests.get(
            url_ics,
            timeout=_REQUEST_TIMEOUT,
            headers={'User-Agent': 'QuilomboAraucaria/1.0'},
            allow_redirects=True,
        )
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error('Falha ao buscar ICS do Google Calendar: %s', e)
        stats['erros'] = 1
        return stats

    if len(response.content) > _MAX_ICS_SIZE:
        logger.error('Arquivo ICS muito grande (%d bytes). Limite: %d bytes.', len(response.content), _MAX_ICS_SIZE)
        stats['erros'] = 1
        return stats

    content_type = response.headers.get('Content-Type', '')
    if 'text/calendar' not in content_type and 'text/plain' not in content_type:
        logger.error(
            'Resposta não é ICS (Content-Type: %s). '
            'Verifique se o Google Calendar está configurado como público.',
            content_type
        )
        stats['erros'] = 1
        return stats

    try:
        cal = Calendar.from_ical(response.content)
    except Exception as e:
        logger.error('Erro ao fazer parsing do ICS: %s', e)
        stats['erros'] = 1
        return stats

    eventos_processados = []

    for componente in cal.walk():
        if componente.name != 'VEVENT':
            continue

        stats['total_ics'] += 1

        try:
            uid = str(componente.get('UID', ''))
            if not uid:
                continue

            summary = str(componente.get('SUMMARY', 'Sem título'))
            description = str(componente.get('DESCRIPTION', ''))
            location = str(componente.get('LOCATION', ''))

            # Tratar data de início
            dtstart = componente.get('DTSTART')
            if dtstart is None:
                continue
            dt_inicio = dtstart.dt

            # Tratar data de término
            dtend = componente.get('DTEND')
            dt_fim = None
            if dtend:
                dt_fim = dtend.dt

            # Converter para date e time conforme tipo
            if isinstance(dt_inicio, datetime):
                if timezone.is_naive(dt_inicio):
                    dt_inicio = timezone.make_aware(dt_inicio)
                data_evento = dt_inicio.date()
                hora_evento = dt_inicio.time()
            elif isinstance(dt_inicio, date):
                data_evento = dt_inicio
                hora_evento = None
            else:
                continue

            if dt_fim and isinstance(dt_fim, datetime):
                if timezone.is_naive(dt_fim):
                    dt_fim = timezone.make_aware(dt_fim)
            elif dt_fim and isinstance(dt_fim, date):
                dt_fim = timezone.make_aware(datetime.combine(dt_fim, time(23, 59)))

            # Limitar tamanhos para segurança
            summary = summary[:250]
            location = location[:300]
            description = description[:5000]

            # Criar ou atualizar evento
            evento, criado = Evento.objects.update_or_create(
                google_event_id=uid,
                defaults={
                    'titulo': summary,
                    'descricao': description,
                    'data': data_evento,
                    'hora': hora_evento,
                    'data_fim': dt_fim,
                    'local': location,
                },
            )

            if criado:
                stats['criados'] += 1
            else:
                stats['atualizados'] += 1

            eventos_processados.append(uid)

        except Exception as e:
            logger.error('Erro ao processar evento ICS (UID=%s): %s', componente.get('UID', '?'), e)
            stats['erros'] += 1

    logger.info(
        'Sincronização concluída: %d eventos no ICS, %d criados, %d atualizados, %d erros',
        stats['total_ics'], stats['criados'], stats['atualizados'], stats['erros']
    )

    return stats
