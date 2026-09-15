from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import FormTarefa
from .models import Tarefa


def _status_filtrado(request):
    status = request.GET.get("status", "")
    return status if status in Tarefa.Status.values else ""


def _exigir_permissao(request, tarefa):
    if request.user != tarefa.criador and request.user != tarefa.responsavel:
        raise PermissionDenied


@login_required
def criar(request):
    if request.method == "POST":
        form = FormTarefa(request.POST)
        if form.is_valid():
            tarefa = form.save(commit=False)
            tarefa.criador = request.user
            tarefa.save()
            messages.success(request, "Tarefa criada com sucesso!")
            return redirect("tarefa_detalhe", tarefa.id)
    else:
        form = FormTarefa()
    return render(
        request, "tarefas/form_tarefa.html", {"form": form, "titulo_pagina": "Nova tarefa"}
    )


@login_required
def detalhe(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, pk=tarefa_id)
    pode_gerenciar = (
        request.user == tarefa.criador or request.user == tarefa.responsavel
    )
    return render(
        request, "tarefas/detalhe.html", {"tarefa": tarefa, "pode_gerenciar": pode_gerenciar}
    )


@login_required
def lista(request):
    tarefas = Tarefa.objects.filter(
        Q(criador=request.user) | Q(responsavel=request.user)
    ).order_by("-criado_em")
    status = _status_filtrado(request)
    if status:
        tarefas = tarefas.filter(status=status)
    return render(
        request, "tarefas/lista.html", {"tarefas": tarefas, "status_atual": status}
    )


@login_required
def dashboard(request):
    status = _status_filtrado(request)
    tarefas = Tarefa.objects.order_by("-criado_em")
    if status:
        tarefas = tarefas.filter(status=status)
    contadores = {
        "total": Tarefa.objects.count(),
        "pendente": Tarefa.objects.filter(status=Tarefa.Status.PENDENTE).count(),
        "andamento": Tarefa.objects.filter(status=Tarefa.Status.ANDAMENTO).count(),
        "concluida": Tarefa.objects.filter(status=Tarefa.Status.CONCLUIDA).count(),
    }
    return render(
        request,
        "tarefas/dashboard.html",
        {"tarefas": tarefas, "contadores": contadores, "status_atual": status},
    )


@login_required
def editar(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, pk=tarefa_id)
    _exigir_permissao(request, tarefa)
    if request.method == "POST":
        form = FormTarefa(request.POST, instance=tarefa)
        if form.is_valid():
            form.save()
            messages.success(request, "Tarefa atualizada com sucesso!")
            return redirect("tarefa_detalhe", tarefa.id)
    else:
        form = FormTarefa(instance=tarefa)
    return render(
        request,
        "tarefas/form_tarefa.html",
        {"form": form, "titulo_pagina": "Editar tarefa"},
    )


@login_required
def excluir(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, pk=tarefa_id)
    _exigir_permissao(request, tarefa)
    if request.method == "POST":
        tarefa.delete()
        messages.success(request, "Tarefa excluída com sucesso!")
        return redirect("dashboard")
    return render(request, "tarefas/confirmar_exclusao.html", {"tarefa": tarefa})
