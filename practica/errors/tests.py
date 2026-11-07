from django.test import TestCase
from django.urls import reverse


class Error404HandlingTests(TestCase):
    """Pruebas para verificar el manejo del error 404 en filtros GET."""

    def test_filtro_categoria_inexistente_retorna_404(self):
        response = self.client.get(reverse('gallery'), {'categoria': 9999})
        self.assertEqual(response.status_code, 404)

    def test_filtro_parametro_no_numerico_retorna_404(self):
        response = self.client.get(reverse('gallery'), {'categoria': 'invalido'})
        self.assertEqual(response.status_code, 404)
