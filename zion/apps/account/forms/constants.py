# Python Standard Library
import re

# Django Imports
from django.contrib.auth import get_user_model


User = get_user_model()
USER_FIELD_MAX_LENGTH = getattr(User, User.USERNAME_FIELD).field.max_length

ALL_NUM_RE = re.compile(r"^[\w\-\.\+]+$")
