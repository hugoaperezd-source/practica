import smtplib
import ssl
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


def _enviar_correo_smtp(host, port, user, password, correo):
    """Envía un EmailMessage por SMTP con respaldo ante certificados SSL locales en Windows."""
    try:
        conexion = get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host=host,
            port=port,
            username=user,
            password=password,
            use_tls=True,
            fail_silently=False,
        )
        correo.connection = conexion
        correo.send(fail_silently=False)
        print(f'[SMTP OK] Correo entregado a la bandeja {user}')
    except Exception as exc_primario:
        try:
            contexto_ssl = ssl._create_unverified_context()
            with smtplib.SMTP(host, port, timeout=10) as servidor:
                servidor.ehlo()
                servidor.starttls(context=contexto_ssl)
                servidor.ehlo()
                servidor.login(user, password)
                servidor.send_message(correo.message())
            print(f'[SMTP OK - SSL Fallback] Correo entregado a la bandeja {user}')
        except Exception as exc_secundario:
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
            # Extrae cada dato ya validado y sanitizado desde el diccionario cleaned_data
            nombre = contact_form.cleaned_data['nombre']
            email = contact_form.cleaned_data['email']
            telefono = contact_form.cleaned_data['telefono']
            motivo = contact_form.cleaned_data['motivo']
            mensaje = contact_form.cleaned_data['mensaje']

            # Construye la lista completa de cuentas SMTP (cuenta principal + cuentas adicionales)
            cuentas_smtp = []
            user_principal = getattr(settings, 'EMAIL_HOST_USER', '').strip()
            pass_principal = getattr(settings, 'EMAIL_HOST_PASSWORD', '').strip()
            if user_principal and pass_principal:
                cuentas_smtp.append((user_principal, pass_principal))

            for cuenta_extra in getattr(settings, 'MAILTRAP_CUENTAS_ADICIONALES', []):
                if len(cuenta_extra) == 2 and cuenta_extra[0].strip() and cuenta_extra[1].strip():
                    par_limpio = (cuenta_extra[0].strip(), cuenta_extra[1].strip())
                    if par_limpio not in cuentas_smtp:
                        cuentas_smtp.append(par_limpio)

            asunto = f'ViajAPP: Nuevo mensaje de contacto ({motivo})'
            cuerpo = (
                f'De: {nombre} <{email}>\n'
                f'Teléfono: {telefono}\n'
                f'Motivo: {motivo}\n\n'
                f'Escribió:\n{mensaje}'
            )

            host = getattr(settings, 'EMAIL_HOST', 'sandbox.smtp.mailtrap.io') or 'sandbox.smtp.mailtrap.io'
            port = int(getattr(settings, 'EMAIL_PORT', 2525) or 2525)

            # Envía un ejemplar independiente con su propia conexión SMTP a cada bandeja configurada
            for idx, (smtp_user, smtp_pass) in enumerate(cuentas_smtp):
                if idx > 0:
                    time.sleep(1.2)
                correo = EmailMessage(
                    subject=asunto,
                    body=cuerpo,
                    from_email='no-contestar@inbox.mailtrap.io',
                    to=['contacto@turismonatural.com'],
                    reply_to=[email],
                )
                _enviar_correo_smtp(host, port, smtp_user, smtp_pass, correo)

            # Redirige a /contact/?ok tras superar todas las validaciones del formulario (Patrón Post/Redirect/Get)
            return redirect(f"{reverse('contact')}?ok")
        else:
            print(f'[Formulario Contacto] Errores de validación: {contact_form.errors.as_text()}')

    # Renderiza la plantilla contact.html enviando el formulario (vacío o con errores de validación)
    return render(request, 'contact/contact.html', {'form': contact_form})


