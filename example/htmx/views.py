from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.views.generic.edit import FormView

from django_edne_cep.forms import CepFormField

from .forms import PedidoForm

TEMPLATE = "htmx/pedido.html"


@require_GET
def cep_details(request):
    field = CepFormField()
    cep_raw = request.GET.get("cep", "")
    template = f"{TEMPLATE}#campos-endereco"

    try:
        cep_obj = field.clean(cep_raw)
    except ValidationError as e:
        return render(
            request,
            template,
            {
                "form": PedidoForm(initial={"cep": cep_raw}),
                "cep_errors": e.error_list,
            },
        )

    return render(
        request,
        template,
        {
            "form": PedidoForm(initial=cep_obj.as_dict()),
            "cep_obj": cep_obj,
        },
    )


class PedidoView(FormView):
    template_name = TEMPLATE
    form_class = PedidoForm

    def form_valid(self, form):
        return render(
            self.request,
            f"{TEMPLATE}#resultado",
            {"pedido": form.cleaned_data},
        )

    def form_invalid(self, form):
        if validated_cep := form.cleaned_data.get("cep", None):
            # request's QueryDict is immutable
            form.data = form.data.copy()
            # skip validated CEP's empty fields to avoid overwriting the user's input
            form.data.update({k: v for k, v in validated_cep.as_dict().items() if v})

        ctx = {
            "form": form,
            "cep_obj": validated_cep,
        }
        template = (
            f"{TEMPLATE}#formulario"
            if self.request.headers.get("HX-Request")
            else TEMPLATE
        )
        return render(self.request, template, ctx)
