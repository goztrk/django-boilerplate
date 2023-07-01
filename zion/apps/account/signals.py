# Django Imports
from django.dispatch import Signal


email_confirmed = Signal()
email_confirmation_sent = Signal()
user_logged_in = Signal()
user_login_attempt = Signal()
