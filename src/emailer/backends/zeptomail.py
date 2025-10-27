# emailer/backends/zeptomail.py
import requests
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail import EmailMultiAlternatives

class ZeptoMailBackend(BaseEmailBackend):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_url = getattr(settings, 'ZEPTOMAIL_API_URL', None)
        self.api_token = getattr(settings, 'ZEPTOMAIL_API_TOKEN', None)
        self.headers = {
            'Authorization': f'Zoho-enczapikey {self.api_token}',
            'Content-Type': 'application/json',
        }

    def _build_payload(self, message):
        payload = {
            "from": {"address": message.from_email},
            "to": [{"email_address": {"address": addr}} for addr in message.to],
            "subject": message.subject,
        }

        if message.body:
            payload['textbody'] = message.body

        if isinstance(message, EmailMultiAlternatives):
            html = next((content for content, mimetype in message.alternatives if mimetype == 'text/html'), None)
            if html:
                payload['htmlbody'] = html

        return payload

    def send_messages(self, email_messages):
        if not self.api_url or not self.api_token:
            if not self.fail_silently:
                raise ValueError("ZeptoMail API URL or token is not configured.")
            return 0

        sent_count = 0
        for message in email_messages:
            try:
                payload = self._build_payload(message)
                response = requests.post(self.api_url, json=payload, headers=self.headers)
                response.raise_for_status()
                sent_count += 1
            except requests.exceptions.RequestException as e:
                if not self.fail_silently:
                    raise e
        return sent_count