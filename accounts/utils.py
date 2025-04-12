from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage, message
from django.conf import settings
import yagmail
def detectUser(user):
    if user.role == 1:
        redirectUrl = 'vendorDashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'custDashboard'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl

    
def send_verification_email(request, user, mail_subject, email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(email_template, {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.content_subtype = "html"
    mail.send()

def send_verification_email(request, user, mail_subject, email_template):
    current_site = get_current_site(request)
    context = {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    }
    message = render_to_string(email_template, context)

    yag = yagmail.SMTP(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    yag.send(
        to=user.email,
        subject=mail_subject,
        contents=message
    )

def send_notification(mail_subject, mail_template, context):
    message = render_to_string(mail_template, context)
    recipient = context['to_email']
    if isinstance(recipient, str):
        recipient = [recipient]

    yag = yagmail.SMTP(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    yag.send(
        to=recipient,
        subject=mail_subject,
        contents=message
    )
