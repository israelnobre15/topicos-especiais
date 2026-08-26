from django.urls import path
from produtos import views

urlpatterns = [
    path("",views.lista_produtos,name="lista_produtos")
]