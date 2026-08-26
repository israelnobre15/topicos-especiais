from django.shortcuts import render
from .models import Produto
# Create your views here.

def lista_produtos(request):
    return render(request=request,template_name="produtos.html",context={"produtos":Produto.objects.all()})