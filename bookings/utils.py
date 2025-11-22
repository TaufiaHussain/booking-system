from io import BytesIO
from django.template import engines, loader
from xhtml2pdf import pisa


def generate_booking_pdf(booking):
    """
    Generate a PDF file (bytes) for a booking using an HTML template.
    """
    html = loader.render_to_string("bookings/booking_pdf.html", {"booking": booking})

    output = BytesIO()
    pisa.CreatePDF(html, dest=output)

    pdf_bytes = output.getvalue()
    output.close()
    return pdf_bytes


def render_email_from_db(key, context):
    """
    Look up EmailTemplate by key and render subject + body using Django templates.
    Returns (subject, body) or (None, None) if not found/active.
    """
    from .models import EmailTemplate  # imported here to avoid circular import

    try:
        tmpl = EmailTemplate.objects.get(key=key, is_active=True)
    except EmailTemplate.DoesNotExist:
        return None, None

    django_engine = engines["django"]

    subject_tmpl = django_engine.from_string(tmpl.subject)
    body_tmpl = django_engine.from_string(tmpl.body)

    subject = subject_tmpl.render(context).strip()
    body = body_tmpl.render(context)

    return subject, body
