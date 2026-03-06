from django.http import JsonResponse

from django_edne_cep import lookup_cep


def cep_view(request, cep):
    result = lookup_cep(cep)

    if result is None:
        return JsonResponse({"error": "CEP not found"}, status=404)

    return JsonResponse(
        {
            "cep": result.cep,
            "logradouro": result.logradouro,
            "complemento": result.complemento,
            "bairro": result.bairro,
            "municipio": result.municipio,
            "municipio_cod_ibge": result.municipio_cod_ibge,
            "uf": result.uf,
        }
    )
