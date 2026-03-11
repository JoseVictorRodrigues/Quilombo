from datetime import date, time
from django.test import TestCase, Client
from django.urls import reverse
from .models import Evento


class EventoModelTest(TestCase):
    def test_criar_evento(self):
        evento = Evento.objects.create(
            titulo='Roda de Conversa',
            descricao='Encontro para debater agroecologia.',
            data=date(2026, 4, 15),
            hora=time(14, 0),
            local='Espaço Cultural',
        )
        self.assertEqual(str(evento), 'Roda de Conversa - 15/04/2026')


class EventoViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.evento = Evento.objects.create(
            titulo='Oficina de Compostagem',
            descricao='Aprenda a fazer compostagem doméstica.',
            data=date(2026, 6, 20),
            hora=time(10, 0),
            local='Horta Comunitária',
        )

    def test_agenda_status(self):
        response = self.client.get(reverse('agenda'))
        self.assertEqual(response.status_code, 200)

    def test_agenda_template(self):
        response = self.client.get(reverse('agenda'))
        self.assertTemplateUsed(response, 'eventos/agenda.html')

    def test_detalhe_evento_status(self):
        response = self.client.get(reverse('detalhe_evento', args=[self.evento.pk]))
        self.assertEqual(response.status_code, 200)

    def test_detalhe_evento_template(self):
        response = self.client.get(reverse('detalhe_evento', args=[self.evento.pk]))
        self.assertTemplateUsed(response, 'eventos/detalhe.html')

    def test_evento_inexistente_404(self):
        response = self.client.get(reverse('detalhe_evento', args=[9999]))
        self.assertEqual(response.status_code, 404)
