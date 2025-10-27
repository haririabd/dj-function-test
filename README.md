# django-emailer

A reusable Django app for sending transactional emails via ZeptoMail, with support for HTML/text bodies, environment-based configuration, and CLI setup.

---

## 🚀 Features

- ZeptoMail integration via Django's email backend
- HTML + plain text email support
- Environment-based config using `python-decouple`
- CLI setup via `python manage.py setup_emailer`
- Mockable API for testing
- Admin metadata injection

---

## 📦 Installation

### 1. Clone or install the app into your Django project:
   
```sh
pip install -e path/to/emailer
```

### 2. Add to `INSTALLED_APPS` in `settings.py`:
    
```sh
INSTALLED_APPS += ['emailer']
```

### 3. Add required settings

```py
from decouple import config

EMAIL_BACKEND = 'emailer.backends.zeptomail.ZeptoMailBackend'

ZEPTOMAIL_API_URL = config('ZEPTOMAIL_API_URL')
ZEPTOMAIL_API_TOKEN = config('ZEPTOMAIL_API_TOKEN')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

ADMIN_USER_NAME = config('ADMIN_USER_NAME', default='Admin')
ADMIN_USER_EMAIL = config('ADMIN_USER_EMAIL', default='admin@email.com')
```

## ⚙️ Setup

Run the interactive setup command:
```sh
python manage.py setup_emailer
```
This will:
- Create or update your `.env` file
- Prompt for ZeptoMail credentials and admin info
- Remind you to update `settings.py`

## 📤 Usage

Import and use the `send_email()` API:

```py
from emailer.api import send_email

send_email(
    to='user@example.com',
    subject='Welcome!',
    text='Thanks for joining.',
    html='<p>Thanks for joining.</p>'
)
```

## 🧪 Testing

To run tests:

```sh
python manage.py test emailer.tests.test_zeptomail
```

Mocked tests are included for backend verification. Real email tests can be run manually via:

```sh
python manage.py sendtestemail --admins
```

## 🧰 Customization

You can override:
- Templates (if added)
- Headers and metadata
- Backend logic via subclassing

## License

This project is licensed under the MIT License.

---