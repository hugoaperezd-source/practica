from django.test import TestCase

from .forms import ContactForm


class ContactFormTests(TestCase):
    """Pruebas unitarias para las validaciones por campo y seguridad de ContactForm."""

    def test_formulario_valido(self):
        form = ContactForm(data={
            'nombre': 'Juan Pérez',
            'email': 'juan.perez@correo.cl',
            'telefono': '+56987654321',
            'motivo': 'rutas',
            'mensaje': 'Hola, me gustaría consultar por las rutas de senderismo en el sur.',
        })
        self.assertTrue(form.is_valid())

    def test_validacion_campos_invalidos_y_seguridad_xss(self):
        form = ContactForm(data={
            'nombre': 'Juan123',
            'email': 'correo-invalido',
            'telefono': '12345',
            'motivo': '',
            'mensaje': '<script>alert("xss")</script> texto corto',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('telefono', form.errors)
        self.assertIn('motivo', form.errors)
        self.assertIn('mensaje', form.errors)

