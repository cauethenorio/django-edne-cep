from django.core.cache import cache

from .models import Cep
from .settings import get_setting


def lookup_cep(cep_str):
    cleaned = cep_str.replace("-", "").strip()

    timeout = get_setting("CACHE_TIMEOUT")

    if timeout > 0:
        cache_key = f"edne:cep:{cleaned}"
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

    result = Cep.objects.filter(cep=cleaned).first()

    if timeout > 0 and result is not None:
        cache.set(cache_key, result, timeout)

    return result
