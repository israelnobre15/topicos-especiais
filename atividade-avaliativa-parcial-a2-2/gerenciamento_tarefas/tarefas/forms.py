from django import forms

from .models import Tarefa


class FormTarefa(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ["titulo", "descricao", "status", "responsavel"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "responsavel": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "titulo": "Título",
            "descricao": "Descrição",
            "status": "Status",
            "responsavel": "Responsável",
        }
