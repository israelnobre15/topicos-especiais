from django.urls import path

from . import views

urlpatterns = [
    path("", views.lista, name="lista_tarefas"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("nova/", views.criar, name="tarefa_criar"),
    path("<int:tarefa_id>/", views.detalhe, name="tarefa_detalhe"),
    path("<int:tarefa_id>/editar/", views.editar, name="tarefa_editar"),
    path("<int:tarefa_id>/excluir/", views.excluir, name="tarefa_excluir"),
]
