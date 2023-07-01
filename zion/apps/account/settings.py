"""
Accounts Settings
"""

USER_MODEL = "accounts.user"

# Fields that can be used as username field
ACCOUNTS_LOGIN_WITH = ["username", "email"]

# User registration requires user to activate their account using
REQUIRE_EMAIL_ACTIVATION = False
