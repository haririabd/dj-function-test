import os
import re
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from dotenv import set_key, dotenv_values

class Command(BaseCommand):
    help = "Interactive setup for django-emailer configuration"

    def add_arguments(self, parser):
        parser.add_argument(
            '--env',
            type=str,
            help='Optional path to .env file (default: auto-detect)'
        )

    def handle(self, *args, **options):
        # Determine .env path
        if options['env']:
            env_path = Path(options['env']).expanduser().resolve()
            self.stdout.write(self.style.NOTICE(f"Using custom .env path: {env_path}"))
        else:
            env_path = Path(settings.BASE_DIR).parent / '.env'
            if not env_path.exists():
                fallback_path = Path(settings.BASE_DIR) / '.env'
                if fallback_path.exists():
                    env_path = fallback_path
            self.stdout.write(self.style.NOTICE(f"Auto-detected .env path: {env_path}"))

        # Create .env if missing
        if not env_path.exists():
            env_path.touch()
            self.stdout.write(self.style.WARNING("Created new .env file"))

        env = dotenv_values(env_path)

        def prompt_and_set(key, prompt, default='', validator=None, note=None):
            current = env.get(key, default)
            if note:
                self.stdout.write(self.style.WARNING(f"Note: {note}"))
            while True:
                value = input(f"{prompt} [{current}]: ") or current
                if validator and not validator(value):
                    self.stdout.write(self.style.ERROR(f"Invalid value for {key}. Please try again."))
                    continue
                set_key(str(env_path), key, value)
                self.stdout.write(self.style.SUCCESS(f"{key} set to: {value}"))
                break

        def is_valid_email(email):
            return re.match(r"[^@]+@[^@]+\.[^@]+", email)

        def is_valid_token(token):
            return len(token.strip()) >= 20

        self.stdout.write(self.style.NOTICE("🔧 Starting django-emailer setup…"))

        prompt_and_set(
            'ZEPTOMAIL_API_URL',
            'Enter ZeptoMail API URL',
            default='https://api.zeptomail.com/v1.1/email'
        )

        prompt_and_set(
            'ZEPTOMAIL_API_TOKEN',
            'Enter your ZeptoMail API token',
            validator=is_valid_token
        )

        prompt_and_set('ADMIN_USER_NAME', 'Enter admin display name')

        prompt_and_set(
            'ADMIN_USER_EMAIL',
            'Enter admin email address',
            validator=is_valid_email
        )

        prompt_and_set(
            'DEFAULT_FROM_EMAIL',
            'Enter default from email',
            validator=is_valid_email,
            note='This must match the sender address configured in your ZeptoMail dashboard.'
        )

        self.stdout.write(self.style.SUCCESS(f"\n✅ Setup complete. Your .env file is now configured at: {env_path}"))

        # Reminder to update settings.py
        self.stdout.write(self.style.WARNING("\n⚠️  Final step: Add the following to your settings.py if not already present:\n"))
        self.stdout.write("""
from decouple import config

EMAIL_BACKEND = 'emailer.backends.zeptomail.ZeptoMailBackend'

ZEPTOMAIL_API_URL = config('ZEPTOMAIL_API_URL')
ZEPTOMAIL_API_TOKEN = config('ZEPTOMAIL_API_TOKEN')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

ADMIN_USER_NAME = config('ADMIN_USER_NAME', default='Admin')
ADMIN_USER_EMAIL = config('ADMIN_USER_EMAIL', default='admin@email.com')
""")