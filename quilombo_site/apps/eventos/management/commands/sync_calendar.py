"""
Management command para sincronizar eventos do Google Calendar.
Uso: python manage.py sync_calendar
Pode ser agendado via cron ou task scheduler.
"""
from django.core.management.base import BaseCommand
from apps.core.models import ConfiguracaoSite
from apps.eventos.sync_calendar import sincronizar_calendario

_DEFAULT_ICS_URL = 'https://calendar.google.com/calendar/ical/quilomboaraucaria%40gmail.com/public/basic.ics'


class Command(BaseCommand):
    help = 'Sincroniza eventos do Google Calendar (ICS) para o banco de dados.'

    def handle(self, *args, **options):
        config = ConfiguracaoSite.get()
        url = config.google_calendar_link or _DEFAULT_ICS_URL

        self.stdout.write(f'Sincronizando calendário: {url}')
        stats = sincronizar_calendario(url)

        self.stdout.write(self.style.SUCCESS(
            f'Concluído: {stats["total_ics"]} eventos no ICS, '
            f'{stats["criados"]} criados, '
            f'{stats["atualizados"]} atualizados, '
            f'{stats["erros"]} erros.'
        ))
