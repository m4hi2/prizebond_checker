import os

from django.core.exceptions import ImproperlyConfigured


def get_env(env_name: str, default_value: str = None) -> str:
    value = os.getenv(env_name, default_value)

    if not value:
        raise ImproperlyConfigured(
            f"{env_name} Environment is not properly configured."
        )
