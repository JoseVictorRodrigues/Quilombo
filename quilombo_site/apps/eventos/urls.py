from django.urls import path
from . import views

urlpatterns = [
    path('', views.agenda, name='agenda'),
    path('<int:pk>/', views.detalhe_evento, name='detalhe_evento'),
]
