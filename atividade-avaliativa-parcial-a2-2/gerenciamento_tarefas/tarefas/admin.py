from django.contrib import admin

from .models import Tarefa


@admin.register(Tarefa)
class AdminTarefa(admin.ModelAdmin):
    list_display = ("titulo", "status", "criador", "responsavel", "criado_em")
    list_filter = ("status",)
    search_fields = ("titulo", "descricao")
