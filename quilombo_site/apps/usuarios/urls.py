from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.equipe_login, name='equipe_login'),
    path('logout/', views.equipe_logout, name='equipe_logout'),
    path('', views.equipe_painel, name='equipe_painel'),
    path('novo-post/', views.equipe_criar_post, name='equipe_criar_post'),
    path('editar-post/<int:pk>/', views.equipe_editar_post, name='equipe_editar_post'),
    path('excluir-post/<int:pk>/', views.equipe_excluir_post, name='equipe_excluir_post'),
    path('excluir-midia/<int:pk>/', views.equipe_excluir_midia, name='equipe_excluir_midia'),
    path('upload-imagem/', views.equipe_upload_imagem, name='equipe_upload_imagem'),
    path('configuracoes/', views.equipe_configuracoes, name='equipe_configuracoes'),
]
