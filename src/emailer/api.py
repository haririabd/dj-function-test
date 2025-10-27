from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_email(to, subject, template=None, context=None, text=None, html=None, from_email=None):
    from_email = from_email or settings.DEFAULT_FROM_EMAIL
    email = EmailMultiAlternatives(subject, text or '', from_email, [to])

    if html:
        email.attach_alternative(html, "text/html")
    elif template:
        from django.template.loader import render_to_string
        html = render_to_string(template, context or {})
        email.attach_alternative(html, "text/html")

    email.send()