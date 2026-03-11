from django.db import models
from apps.core.models import validar_imagem


class Evento(models.Model):
    titulo = models.CharField('Título', max_length=250)
    descricao = models.TextField('Descrição', blank=True, default='')
    data = models.DateField('Data')
    hora = models.TimeField('Hora', blank=True, null=True)
    data_fim = models.DateTimeField('Data/hora de término', blank=True, null=True)
    local = models.CharField('Local', max_length=300, blank=True, default='')
    imagem = models.ImageField(
        'Imagem',
        upload_to='eventos/',
        blank=True,
        null=True,
        validators=[validar_imagem]
    )
    google_event_id = models.CharField(
        'ID do Google Calendar',
        max_length=512,
        blank=True,
        null=True,
        unique=True,
        db_index=True,
        help_text='Identificador único do evento no Google Calendar (preenchido automaticamente na sincronização).'
    )
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['data', 'hora']

    def __str__(self):
        return f'{self.titulo} - {self.data:%d/%m/%Y}'
