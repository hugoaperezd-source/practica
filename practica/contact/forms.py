# Importa expresiones regulares para limpiar espacios en el teléfono
import re
# Importa el módulo forms de Django para construir el formulario
from django import forms
# Importa validadores nativos de Django para correo, longitud y expresiones regulares
from django.core.validators import EmailValidator, MaxLengthValidator, MinLengthValidator, RegexValidator
# Importa strip_tags para eliminar cualquier etiqueta HTML maliciosa (prevención de XSS)
from django.utils.html import strip_tags


class ContactForm(forms.Form):
    """Formulario de contacto con validaciones por campo y normas de codificación segura."""

    # Lista de opciones válidas para el campo desplegable 'motivo'
    MOTIVO_CHOICES = [
        ('', 'Selecciona un motivo de contacto...'),
        ('rutas', 'Consulta sobre rutas y destinos'),
        ('resena', 'Sugerir un nuevo destino o reseña'),
        ('ecoturismo', 'Información de ecoturismo y seguridad'),
        ('otro', 'Otra consulta general'),
    ]

    # Validador que exige únicamente letras (incluyendo tildes y ñ) y espacios en el nombre
    solo_letras_validator = RegexValidator(
        regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$',
        message='El nombre solo puede contener letras y espacios (sin números ni símbolos).',
    )

    # Validador que verifica que el teléfono contenga números, espacios o '+' opcional
    telefono_validator = RegexValidator(
        regex=r'^\+?[\d\s\-]{8,18}$',
        message='Ingresa un teléfono válido de 8 a 15 dígitos (solo números y signo + opcional).',
    )

    # Campo 1: Nombre (obligatorio, entre 2 y 80 caracteres, solo letras)
    nombre = forms.CharField(
        label='Nombre Completo',
        min_length=2,
        max_length=80,
        required=True,
        validators=[
            MinLengthValidator(2, message='El nombre debe tener al menos 2 caracteres.'),
            MaxLengthValidator(80, message='El nombre no puede superar los 80 caracteres.'),
            solo_letras_validator,
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Juan Pérez',
            'autocomplete': 'name',
        }),
        error_messages={
            'required': 'El campo nombre es obligatorio.',
        },
    )

    # Campo 2: Correo electrónico (obligatorio, validado por formato de email)
    email = forms.EmailField(
        label='Correo Electrónico',
        max_length=120,
        required=True,
        validators=[
            EmailValidator(message='Ingresa una dirección de correo electrónico con formato válido.'),
        ],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@correo.cl',
            'autocomplete': 'email',
        }),
        error_messages={
            'required': 'El correo electrónico es obligatorio.',
            'invalid': 'Ingresa una dirección de correo electrónico válida.',
        },
    )

    # Campo 3: Teléfono de contacto (obligatorio, entre 8 y 18 caracteres permitiendo espacios)
    telefono = forms.CharField(
        label='Teléfono de Contacto',
        min_length=8,
        max_length=18,
        required=True,
        validators=[telefono_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+56 9 1234 5678',
            'autocomplete': 'tel',
        }),
        error_messages={
            'required': 'El teléfono de contacto es obligatorio.',
        },
    )

    # Campo 4: Motivo de la consulta (obligatorio, selección desde lista cerrada)
    motivo = forms.ChoiceField(
        label='Motivo de Contacto',
        choices=MOTIVO_CHOICES,
        initial='rutas',
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        error_messages={
            'required': 'Debes seleccionar un motivo de contacto.',
            'invalid_choice': 'Selecciona una opción válida de la lista.',
        },
    )

    # Campo 5: Mensaje de texto (obligatorio, entre 5 y 500 caracteres)
    mensaje = forms.CharField(
        label='Mensaje',
        min_length=5,
        max_length=500,
        required=True,
        validators=[
            MinLengthValidator(5, message='El mensaje debe contener al menos 5 caracteres.'),
            MaxLengthValidator(500, message='El mensaje no puede exceder los 500 caracteres.'),
        ],
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Escribe tu consulta o comentario (mínimo 5 caracteres)...',
        }),
        error_messages={
            'required': 'El mensaje no puede estar vacío.',
        },
    )

    def clean_nombre(self):
        """Valida y sanitiza el nombre evitando etiquetas HTML o espacios vacíos."""
        # Obtiene el nombre ingresado y elimina espacios al inicio y al final
        nombre = self.cleaned_data.get('nombre', '').strip()
        # Elimina cualquier posible etiqueta HTML para prevenir inyección
        nombre_limpio = strip_tags(nombre)
        # Comprueba si el texto original tenía etiquetas HTML comparándolo con el texto limpio
        if nombre != nombre_limpio:
            # Lanza un error de validación si se detectaron etiquetas HTML en el nombre
            raise forms.ValidationError('No se permiten etiquetas HTML ni código en el nombre.')
        # Devuelve el nombre limpio y seguro
        return nombre_limpio

    def clean_email(self):
        """Normaliza y valida el dominio del correo electrónico."""
        # Convierte el correo a minúsculas y quita espacios
        email = self.cleaned_data.get('email', '').strip().lower()
        # Lista negra de dominios de correos temporales no permitidos
        dominios_bloqueados = {'tempmail.com', 'mailinator.com', '10minutemail.com'}
        # Extrae la parte del dominio después del símbolo @
        dominio = email.split('@')[-1] if '@' in email else ''
        # Verifica si el dominio del correo pertenece a la lista de dominios bloqueados
        if dominio in dominios_bloqueados:
            # Lanza un error de validación rechazando correos temporales
            raise forms.ValidationError('No se permiten correos temporales o desechables.')
        # Devuelve el correo electrónico normalizado
        return email

    def clean_telefono(self):
        """Normaliza el teléfono eliminando espacios o guiones intermedios y valida cantidad de dígitos."""
        # Quita cualquier espacio o guion intermedio del número telefónico
        telefono = re.sub(r'[\s\-]+', '', self.cleaned_data.get('telefono', ''))
        # Extrae únicamente los dígitos quitando el signo '+' inicial si existe
        digitos = telefono.lstrip('+')
        # Verifica que solo queden dígitos numéricos y que su longitud esté entre 8 y 15
        if not digitos.isdigit() or not (8 <= len(digitos) <= 15):
            # Lanza error si la cantidad de dígitos no es válida
            raise forms.ValidationError('El teléfono debe contener entre 8 y 15 dígitos numéricos.')
        # Devuelve el número telefónico normalizado
        return telefono

    def clean_mensaje(self):
        """Sanitiza el mensaje previniendo inyección de etiquetas HTML/scripts (XSS)."""
        # Obtiene el mensaje sin espacios sobrantes en los extremos
        mensaje = self.cleaned_data.get('mensaje', '').strip()
        # Rechaza el mensaje si contiene símbolos '<', '>' o etiquetas HTML/JavaScript
        if '<' in mensaje or '>' in mensaje or strip_tags(mensaje) != mensaje:
            # Lanza un error de validación por intento de inyección HTML/XSS
            raise forms.ValidationError('Por seguridad, el mensaje no puede contener etiquetas HTML ni scripts.')
        # Devuelve el mensaje validado y seguro
        return mensaje

