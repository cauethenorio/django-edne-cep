from django.core.cache import caches

from .models import Cep
from .settings import get_setting
from .validators import validate_cep_format

# sentinel to distinguish a cache miss from a cached None result
_CACHE_MISS = object()

_CACHE_KEY_FORMAT = "edne:cep:{}"


def lookup_cep(cep_str: str) -> Cep | None:
    cleaned_cep = cep_str.replace("-", "").strip()
    validate_cep_format(cleaned_cep)

    timeout = get_setting("CACHE_TIMEOUT")
    cache = caches[get_setting("CACHE_ALIAS")]
    cache_key = _CACHE_KEY_FORMAT.format(cleaned_cep)

    if timeout > 0:
        # use sentinel as default so we can tell apart "not in cache" from "cached None"
        cached = cache.get(cache_key, _CACHE_MISS)
        if cached is not _CACHE_MISS:
            return cached

    result = Cep.objects.filter(cep=cleaned_cep).first()

    if timeout > 0:
        # cache both found and not-found results to avoid repeated DB hits
        cache.set(cache_key, result, timeout)

    return result
