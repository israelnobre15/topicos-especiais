from django.conf import settings
from django.db import models


class Tarefa(models.Model):
    class Status(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        ANDAMENTO = "andamento", "Em andamento"
        CONCLUIDA = "concluida", "Concluída"

    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDENTE
    )
    criador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tarefas_criadas",
    )
    responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tarefas_atribuidas",
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    @property
    def classe_badge(self):
        return {
            self.Status.PENDENTE: "text-bg-warning",
            self.Status.ANDAMENTO: "text-bg-info",
            self.Status.CONCLUIDA: "text-bg-success",
        }[self.status]
