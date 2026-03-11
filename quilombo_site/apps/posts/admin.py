from django.contrib import admin
from .models import Post, MediaPost


class MediaPostInline(admin.TabularInline):
    model = MediaPost
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'data_publicacao', 'publicado')
    list_filter = ('publicado', 'data_publicacao', 'autor')
    search_fields = ('titulo', 'conteudo', 'resumo')
    prepopulated_fields = {'slug': ('titulo',)}
    list_editable = ('publicado',)
    date_hierarchy = 'data_publicacao'
    inlines = [MediaPostInline]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.autor = request.user
        super().save_model(request, obj, form, change)


@admin.register(MediaPost)
class MediaPostAdmin(admin.ModelAdmin):
    list_display = ('post', 'tipo', 'ordem')
    list_filter = ('tipo',)
