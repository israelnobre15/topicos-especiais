from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect, render

from .forms import FormCadastro


def cadastro(request):
    if request.method == "POST":
        form = FormCadastro(request.POST)
        if form.is_valid():
            dados = form.cleaned_data
            usuario = User.objects.create_user(
                username=dados["email"],
                email=dados["email"],
                password=dados["senha"],
                first_name=dados["nome"],
            )
            auth_login(request, usuario)
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = FormCadastro()
    return render(request, "usuarios/cadastro.html", {"form": form})


def entrar(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        usuario = authenticate(request, username=email, password=senha)
        if usuario is not None:
            auth_login(request, usuario)
            messages.success(request, f"Bem-vindo(a), {usuario.first_name}!")
            return redirect(settings.LOGIN_REDIRECT_URL)
        messages.error(request, "E-mail ou senha inválidos.")
    return render(request, "usuarios/login.html")


@login_required
def sair(request):
    if request.method == "POST":
        auth_logout(request)
        messages.success(request, "Sessão encerrada com sucesso.")
        return redirect(settings.LOGOUT_REDIRECT_URL)
    return HttpResponseNotAllowed(["POST"])
