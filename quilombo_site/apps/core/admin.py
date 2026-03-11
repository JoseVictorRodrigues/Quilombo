from django.contrib import admin
from .models import Contato, PontoMapa, ConfiguracaoSite, FotoGaleria


@admin.register(ConfiguracaoSite)
class ConfiguracaoSiteAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    fieldsets = (
        ('Logo', {
            'fields': ('logo', 'tamanho_logo'),
        }),
        ('Aparência', {
            'fields': ('imagem_fundo', 'cor_fundo', 'animacao_folhas_ativa', 'menu_posicao'),
        }),
        ('Redes Sociais', {
            'fields': ('link_instagram', 'link_telegram', 'link_youtube'),
        }),
        ('Contato', {
            'fields': ('email_contato',),
        }),
        ('Integrações', {
            'fields': ('google_calendar_link',),
        }),
    )

    def has_add_permission(self, request):
        return not ConfiguracaoSite.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'data_envio', 'lida')
    list_filter = ('lida', 'data_envio')
    search_fields = ('nome', 'email', 'mensagem')
    readonly_fields = ('nome', 'email', 'mensagem', 'data_envio')
    list_editable = ('lida',)

    def has_add_permission(self, request):
        return False


@admin.register(PontoMapa)
class PontoMapaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'latitude', 'longitude', 'icone')
    search_fields = ('nome',)


@admin.register(FotoGaleria)
class FotoGaleriaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ordem', 'criado_em')
    list_editable = ('ordem',)
    search_fields = ('titulo', 'descricao')
