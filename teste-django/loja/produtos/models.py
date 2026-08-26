from django.db import models

# Create your models here.

class Produto(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=5,decimal_places=2)

    def __str__(self):
        return self.nome