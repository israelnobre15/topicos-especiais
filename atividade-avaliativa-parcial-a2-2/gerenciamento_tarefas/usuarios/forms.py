from django import forms
from django.contrib.auth.models import User


class FormCadastro(forms.Form):
    nome = forms.CharField(
        max_length=100,
        label="Nome",
        widget=forms.TextInput(attrs={"class": "form-control", "autofocus": True}),
    )
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    confirmar_senha = forms.CharField(
        label="Confirmar senha",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado.")
        return email

    def clean(self):
        dados = super().clean()
        senha = dados.get("senha")
        confirmar = dados.get("confirmar_senha")
        if senha and confirmar and senha != confirmar:
            self.add_error("confirmar_senha", "As senhas não conferem.")
        return dados
