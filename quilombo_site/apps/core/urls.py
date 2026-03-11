from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    path('contato/', views.contato, name='contato'),
    path('api/eventos/', views.eventos_api, name='eventos_api'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('favicon.ico', views.favicon, name='favicon'),
]
