# coding: utf-8

# DJANGO IMPORTS
from django.conf import settings

# Admin Site Title
ADMIN_HEADLINE = getattr(settings, "OBY_ADMIN_HEADLINE", 'OBY Studio')
ADMIN_TITLE = getattr(settings, "OBY_ADMIN_TITLE", 'OBY Studio')

# Link to your Main Admin Site (no slashes at start and end)
# not needed anymore
ADMIN_URL = getattr(settings, "OBY_ADMIN_URL", '/admin/')

# Autocomplete Limit
AUTOCOMPLETE_LIMIT = getattr(settings, "OBY_AUTOCOMPLETE_LIMIT", 10)
# Alternative approach to define autocomplete search fields
AUTOCOMPLETE_SEARCH_FIELDS = getattr(settings, "OBY_AUTOCOMPLETE_SEARCH_FIELDS", {})

# SWITCH_USER: Set True in order to activate this functionality
SWITCH_USER = getattr(settings, "OBY_SWITCH_USER", False)
# SWITCH_USER_ORIGINAL: Defines if a user is allowed to login as another user.
# Gets a user object and returns True/False.
SWITCH_USER_ORIGINAL = getattr(settings, "OBY_SWITCH_USER_ORIGINAL", lambda user: user.is_superuser)
# SWITCH_USER_ORIGINAL: Defines if a user is a valid target.
# Gets a user object and returns True/False.
SWITCH_USER_TARGET = getattr(settings, "OBY_SWITCH_USER_TARGET", lambda original_user, user: user.is_staff and not user.is_superuser)

# CLEAN INPUT TYPES
# Replaces input types: search, email, url, tel, number, range, date
# month, week, time, datetime, datetime-local, color
# due to browser inconsistencies.
# see see https://code.djangoproject.com/ticket/23075
CLEAN_INPUT_TYPES = getattr(settings, "OBY_CLEAN_INPUT_TYPES", True)
