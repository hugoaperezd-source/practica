# Importa smtplib para el protocolo de envío de correo SMTP de respaldo
import smtplib
# Importa ssl para gestionar el contexto de certificados TLS/SSL en entornos locales
import ssl
# Importa time para añadir una breve pausa entre envíos y respetar el límite de Mailtrap
import time
# Importa configuración global de settings.py
from django.conf import settings
# Importa EmailMessage y get_connection para construir y enviar correos a una o varias cuentas de Mailtrap
from django.core.mail import EmailMessage, get_connection
# Importa funciones para redireccionar URLs y renderizar plantillas HTML
from django.shortcuts import redirect, render
# Importa reverse para obtener la URL a partir del nombre de la ruta ('contact')
from django.urls import reverse
# Importa el decorador que restringe la vista únicamente a peticiones seguras GET y POST
from django.views.decorators.http import require_http_methods

# Importa el formulario ContactForm creado con sus validaciones en forms.py
from .forms import ContactForm


# Define una función auxiliar privada para enviar el correo por SMTP a una bandeja de Mailtrap
def _enviar_correo_smtp(host, port, user, password, correo):
    """Envía un EmailMessage por SMTP con respaldo ante certificados SSL locales en Windows."""
    # Intenta enviar el correo utilizando el backend SMTP nativo de Django
    try:
        # Crea una conexión SMTP dedicada usando el host, puerto y credenciales de la cuenta
        conexion = get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host=host,
            port=port,
            username=user,
            password=password,
            use_tls=True,
            fail_silently=False,
        )
        # Asigna la conexión recién creada al objeto EmailMessage
        correo.connection = conexion
        # Ejecuta el envío del correo electrónico a través de la conexión SMTP
        correo.send(fail_silently=False)
        # Muestra confirmación en la terminal indicando que el correo se entregó a esa bandeja
        print(f'[SMTP OK] Correo entregado a la bandeja {user}')
    # Captura cualquier error de conexión o certificado del intento primario
    except Exception as exc_primario:
        # Inicia un segundo intento de respaldo usando smtplib con contexto SSL flexible
        try:
            # Crea un contexto SSL sin verificación estricta para evitar bloqueos de certificados locales en Windows
            contexto_ssl = ssl._create_unverified_context()
            # Abre la conexión directa con el servidor SMTP de Mailtrap con espera máxima de 10 segundos
            with smtplib.SMTP(host, port, timeout=10) as servidor:
                # Saluda al servidor SMTP identificando al cliente
                servidor.ehlo()
                # Inicia el cifrado TLS en la conexión usando el contexto SSL creado
                servidor.starttls(context=contexto_ssl)
                # Vuelve a identificar al cliente tras activar el canal cifrado TLS
                servidor.ehlo()
                # Autentica la sesión con el usuario y contraseña de la bandeja de Mailtrap
                servidor.login(user, password)
                # Envía el mensaje MIME construido por el objeto EmailMessage de Django
                servidor.send_message(correo.message())
            # Muestra confirmación en la terminal si el respaldo SSL entregó el correo con éxito
            print(f'[SMTP OK - SSL Fallback] Correo entregado a la bandeja {user}')
        # Si ambos métodos fallan, registra el aviso únicamente en la consola sin interrumpir al usuario
        except Exception as exc_secundario:
            # Imprime el detalle técnico en la terminal del servidor para diagnóstico
            print(f'[SMTP Aviso] No se pudo entregar a {user}: {exc_primario} / {exc_secundario}')


# Restringe la vista para aceptar únicamente los métodos HTTP GET y POST
@require_http_methods(['GET', 'POST'])
def contact(request):
    """Vista del formulario de contacto con validaciones seguras y envío por Mailtrap."""
    # Instancia un formulario vacío por defecto (para cuando el usuario entra por método GET)
    contact_form = ContactForm()

    # Verifica si el usuario envió datos presionando el botón del formulario (método POST)
    if request.method == 'POST':
        # Rellena el formulario con los datos enviados por el usuario en request.POST
        contact_form = ContactForm(data=request.POST)
        # Ejecuta todas las validaciones de campos y métodos clean_<campo>() del formulario
        if contact_form.is_valid():
            # Extrae el nombre validado y sanitizado desde el diccionario cleaned_data
            nombre = contact_form.cleaned_data['nombre']
            # Extrae el correo electrónico validado y normalizado desde cleaned_data
            email = contact_form.cleaned_data['email']
            # Extrae el teléfono validado y sin espacios desde cleaned_data
            telefono = contact_form.cleaned_data['telefono']
            # Extrae el motivo seleccionado de la lista cerrada desde cleaned_data
            motivo = contact_form.cleaned_data['motivo']
            # Extrae el mensaje libre de etiquetas HTML desde cleaned_data
            mensaje = contact_form.cleaned_data['mensaje']

            # Inicializa la lista donde se guardarán todas las cuentas SMTP de Mailtrap configuradas
            cuentas_smtp = []
            # Obtiene el usuario principal de Mailtrap desde settings.py eliminando espacios sobrantes
            user_principal = getattr(settings, 'EMAIL_HOST_USER', '').strip()
            # Obtiene la contraseña principal de Mailtrap desde settings.py eliminando espacios sobrantes
            pass_principal = getattr(settings, 'EMAIL_HOST_PASSWORD', '').strip()
            # Si el usuario y contraseña principales existen, los añade a la lista de cuentas SMTP
            if user_principal and pass_principal:
                # Agrega la tupla (usuario, contraseña) de la cuenta principal
                cuentas_smtp.append((user_principal, pass_principal))

            # Recorre las cuentas adicionales de Mailtrap configuradas para los demás integrantes del equipo
            for cuenta_extra in getattr(settings, 'MAILTRAP_CUENTAS_ADICIONALES', []):
                # Verifica que cada cuenta adicional tenga exactamente usuario y contraseña no vacíos
                if len(cuenta_extra) == 2 and cuenta_extra[0].strip() and cuenta_extra[1].strip():
                    # Limpia espacios en blanco del usuario y contraseña adicionales
                    par_limpio = (cuenta_extra[0].strip(), cuenta_extra[1].strip())
                    # Evita duplicar la cuenta si ya estaba registrada en la lista
                    if par_limpio not in cuentas_smtp:
                        # Añade la cuenta adicional a la lista de envíos
                        cuentas_smtp.append(par_limpio)

            # Construye el asunto del correo indicando el motivo de la consulta
            asunto = f'ViajAPP: Nuevo mensaje de contacto ({motivo})'
            # Construye el cuerpo del mensaje con todos los datos validados del remitente
            cuerpo = (
                f'De: {nombre} <{email}>\n'
                f'Teléfono: {telefono}\n'
                f'Motivo: {motivo}\n\n'
                f'Escribió:\n{mensaje}'
            )

            # Obtiene el host SMTP desde settings.py (por defecto sandbox.smtp.mailtrap.io)
            host = getattr(settings, 'EMAIL_HOST', 'sandbox.smtp.mailtrap.io') or 'sandbox.smtp.mailtrap.io'
            # Obtiene el puerto SMTP convertido a número entero desde settings.py (por defecto 2525)
            port = int(getattr(settings, 'EMAIL_PORT', 2525) or 2525)

            # Recorre cada cuenta de Mailtrap para enviar un ejemplar independiente a cada bandeja
            for idx, (smtp_user, smtp_pass) in enumerate(cuentas_smtp):
                # Si es la segunda cuenta en adelante, espera 1.2 segundos para respetar el límite del plan gratuito de Mailtrap
                if idx > 0:
                    # Pausa breve entre envíos consecutivos
                    time.sleep(1.2)
                # Crea una instancia nueva de EmailMessage con remitente, destinatario y dirección de respuesta
                correo = EmailMessage(
                    subject=asunto,
                    body=cuerpo,
                    from_email='no-contestar@inbox.mailtrap.io',
                    to=['contacto@turismonatural.com'],
                    reply_to=[email],
                )
                # Llama a la función auxiliar para entregar el correo a la bandeja actual
                _enviar_correo_smtp(host, port, smtp_user, smtp_pass, correo)

            # Redirige a /contact/?ok tras superar todas las validaciones del formulario (Patrón Post/Redirect/Get)
            return redirect(f"{reverse('contact')}?ok")
        else:
            # Si algún campo no pasó la validación, muestra el detalle en la terminal para depuración
            print(f'[Formulario Contacto] Errores de validación: {contact_form.errors.as_text()}')

    # Renderiza la plantilla contact.html enviando el formulario (vacío o con errores de validación)
    return render(request, 'contact/contact.html', {'form': contact_form})


