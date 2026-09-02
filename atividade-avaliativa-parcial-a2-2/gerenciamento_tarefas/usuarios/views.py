from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from .models import Usuario
from django.shortcuts import redirect
from django.contrib import messages

def cadastro(request):
    if request.method == "GET":
        return render(request, "cadastro.html")

    nome = request.POST.get("nome")
    email = request.POST.get("email")
    senha = request.POST.get("senha")

    if Usuario.objects.filter(email=email).exists():
        messages.error(request, "Este email já está cadastrado.")
        return redirect("cadastro")  # volta para a página com mensagem de erro

    try:
        Usuario.objects.create(nome=nome, email=email, senha=senha)
        messages.success(request, "Cadastro realizado com sucesso!")
    except Exception as e:
        messages.error(request, f"Erro ao cadastrar: {e}")

    return redirect("cadastro")  # sempre redireciona (GET) para limpar o formulário


def login(request):
    return render(request=request,template_name="login.html")