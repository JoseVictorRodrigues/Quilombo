from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from apps.core.models import validar_imagem
import os


def validar_midia(arquivo):
    """Valida uploads de imagem ou vídeo."""
    ext = os.path.splitext(arquivo.name)[1].lower()
    extensoes_imagem = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    extensoes_video = ['.mp4', '.webm', '.ogg', '.mov']
    extensoes_permitidas = extensoes_imagem + extensoes_video
    if ext not in extensoes_permitidas:
        raise ValidationError(
            f'Formato não permitido. Use: {", ".join(extensoes_permitidas)}'
        )
    # Imagens: max 5MB, Vídeos: max 100MB
    if ext in extensoes_imagem and arquivo.size > 5 * 1024 * 1024:
        raise ValidationError('Imagem muito grande. Máximo: 5MB.')
    if ext in extensoes_video and arquivo.size > 100 * 1024 * 1024:
        raise ValidationError('Vídeo muito grande. Máximo: 100MB. Considere usar um link externo.')


class Post(models.Model):
    titulo = models.CharField('Título', max_length=250)
    slug = models.SlugField('Slug', max_length=260, unique=True, blank=True)
    conteudo = models.TextField('Conteúdo')
    resumo = models.TextField('Resumo', max_length=500)
    data_publicacao = models.DateTimeField('Data de publicação', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    autor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Autor'
    )
    imagem_capa = models.ImageField(
        'Imagem de capa',
        upload_to='posts/',
        blank=True,
        null=True,
        validators=[validar_imagem]
    )
    video_url = models.URLField(
        'URL do vídeo (opcional)',
        blank=True,
        help_text='Ex: https://www.youtube.com/watch?v=...'
    )
    publicado = models.BooleanField('Publicado', default=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-data_publicacao']

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.titulo)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class MediaPost(models.Model):
    TIPO_CHOICES = [
        ('imagem', 'Imagem'),
        ('video', 'Vídeo'),
    ]
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='midias',
        verbose_name='Post'
    )
    arquivo = models.FileField(
        'Arquivo',
        upload_to='posts/midias/',
        validators=[validar_midia],
        blank=True,
        null=True,
    )
    video_url = models.URLField(
        'URL do vídeo externo',
        blank=True,
        default='',
        help_text='Link de vídeo externo (YouTube, Vimeo, etc.)'
    )
    tipo = models.CharField(
        'Tipo',
        max_length=10,
        choices=TIPO_CHOICES,
        default='imagem'
    )
    ordem = models.PositiveIntegerField('Ordem', default=0)

    class Meta:
        ordering = ['ordem']
        verbose_name = 'Mídia do Post'
        verbose_name_plural = 'Mídias do Post'

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.post.titulo}'
