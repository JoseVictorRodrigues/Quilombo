import os
from django.db import models
from django.core.exceptions import ValidationError


def validar_imagem(arquivo):
    """Validação segura de uploads de imagem."""
    ext = os.path.splitext(arquivo.name)[1].lower()
    extensoes_permitidas = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    if ext not in extensoes_permitidas:
        raise ValidationError(
            f'Formato não permitido. Use: {", ".join(extensoes_permitidas)}'
        )
    if arquivo.size > 5 * 1024 * 1024:
        raise ValidationError('Arquivo muito grande. Máximo: 5MB.')


class ConfiguracaoSite(models.Model):
    logo = models.ImageField(
        'Logo do site',
        upload_to='site/',
        blank=True,
        null=True,
        validators=[validar_imagem],
        help_text='Logo circular exibida no topo e hero. Recomendado: 200x200px.'
    )
    tamanho_logo = models.PositiveIntegerField(
        'Tamanho do logo (px)',
        default=120,
        help_text='Tamanho em pixels do logo no hero. Padrão: 120.'
    )
    imagem_fundo = models.ImageField(
        'Imagem de fundo',
        upload_to='site/',
        blank=True,
        null=True,
        validators=[validar_imagem],
        help_text='Imagem de fundo do site. Exibida com overlay semi-transparente.'
    )
    cor_fundo = models.CharField(
        'Cor de fundo',
        max_length=25,
        default='#f5f1eb',
        blank=True,
        help_text='Cor de fundo do site (hex). Usada se não houver imagem de fundo.'
    )
    link_instagram = models.URLField(
        'Link do Instagram',
        blank=True,
        default='',
        help_text='URL completa do perfil no Instagram.'
    )
    link_telegram = models.URLField(
        'Link do Telegram',
        blank=True,
        default='',
        help_text='URL do grupo ou canal no Telegram.'
    )
    link_youtube = models.URLField(
        'Link do YouTube',
        blank=True,
        default='',
        help_text='URL do canal no YouTube.'
    )
    google_calendar_link = models.URLField(
        'Link do Google Calendar',
        blank=True,
        default='',
        help_text='URL pública do Google Calendar para sincronização de eventos.'
    )
    email_contato = models.EmailField(
        'E-mail de contato',
        blank=True,
        default='',
        help_text='E-mail exibido no rodapé e na página de contato.'
    )
    animacao_folhas_ativa = models.BooleanField(
        'Animação de folhas ativa',
        default=True,
        help_text='Ativa ou desativa a animação de folhas caindo no site.'
    )

    class Meta:
        verbose_name = 'Configuração do Site'
        verbose_name_plural = 'Configuração do Site'

    def __str__(self):
        return 'Configuração do Site'

    def save(self, *args, **kwargs):
        # Garante apenas uma instância (singleton)
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Contato(models.Model):
    nome = models.CharField('Nome', max_length=150)
    email = models.EmailField('E-mail')
    mensagem = models.TextField('Mensagem')
    data_envio = models.DateTimeField('Data de envio', auto_now_add=True)
    lida = models.BooleanField('Lida', default=False)

    class Meta:
        verbose_name = 'Mensagem de Contato'
        verbose_name_plural = 'Mensagens de Contato'
        ordering = ['-data_envio']

    def __str__(self):
        return f'{self.nome} - {self.email} ({self.data_envio:%d/%m/%Y})'


class PontoMapa(models.Model):
    nome = models.CharField('Nome do ponto', max_length=200)
    descricao = models.TextField('Descrição', blank=True)
    latitude = models.FloatField('Latitude')
    longitude = models.FloatField('Longitude')
    icone = models.CharField(
        'Ícone',
        max_length=50,
        default='leaf',
        help_text='Nome do ícone Lucide (ex: leaf, home, users)'
    )

    class Meta:
        verbose_name = 'Ponto no Mapa'
        verbose_name_plural = 'Pontos no Mapa'

    def __str__(self):
        return self.nome
