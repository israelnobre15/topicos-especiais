# Classe responsavel pela manipulação de atributos internos de um livro
class Livro:

    def __init__(self,codigo:int, titulo:str,autor:str,ano_publicacao:int, status: str = "Disponível"):
        self.codigo = codigo
        self.titulo = titulo
        self.autor = autor
        self.ano_publicacao = ano_publicacao
        self.status = status

    def emprestar(self)-> bool:
        # Setter de alteração de valores
        if self.status != "Disponível":
            return False
        self.status = "Emprestado"
        return True

    def devolver(self) -> bool:
        # Setter de alteração de valores
        if self.status != "Emprestado":
            return False
        self.status="Disponível"
        return True