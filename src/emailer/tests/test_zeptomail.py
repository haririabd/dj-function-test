from django.test import TestCase, override_settings
from unittest.mock import patch
from emailer.api import send_email

@override_settings(EMAIL_BACKEND='emailer.backends.zeptomail.ZeptoMailBackend')
class ZeptoMailTests(TestCase):
    @patch('emailer.backends.zeptomail.requests.post')
    def test_send_email(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'message': 'Email sent successfully'}

        send_email(
            to='alharir@gmail.com',
            subject='Mocked Email',
            text='Hello world',
            html='<p>Hello world</p>'
        )

        self.assertTrue(mock_post.called)
        self.assertEqual(mock_post.call_count, 1)