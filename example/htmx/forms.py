from django import forms

from django_edne_cep.forms import CepFormField


class PedidoForm(forms.Form):
    nome = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"autocomplete": "name"}),
        initial="Fulano",
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"autocomplete": "email", "inputmode": "email"}),
        initial="fulano@example.com",
    )

    cep = CepFormField()
    logradouro = forms.CharField(max_length=100)
    numero = forms.CharField(label="Número", max_length=10)
    bairro = forms.CharField(max_length=72)
    complemento = forms.CharField(max_length=100, required=False)
    municipio = forms.CharField(label="Cidade", max_length=72)
    uf = forms.CharField(label="UF", max_length=2)
