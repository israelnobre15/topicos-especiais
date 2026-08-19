from livros.livro import Livro 
from typing import Dict, Callable, List

class Biblioteca:

    def __init__(self):
        self.estoque: List[Livro] = []
        self.opcoes: Dict[str, Callable[[], None]] = {
            "1": self.cadastrar,
            "2": self.consultar,
            "3": self.listar,
            "4": self.emprestar,
            "5": self.devolver,
            "6": self.excluir,
            "7": self.sair,
        }

    def consultar_por_id(self, codigo: int) -> Livro:
        livro = next((livro for livro in self.estoque if livro.codigo == codigo), None)

        if not livro:
            raise ValueError(f"Livro com codigo {codigo} nao encontrado!")

        return livro

    def consultar(self,codigo:int):
        print(self.consultar_por_id(codigo=codigo).__dict__)

    def cadastrar(self, codigo: int, titulo: str, autor: str, ano_publicacao: int) -> bool:
        try:
            self.consultar_por_id(codigo=codigo)
            print(f"Livro com codigo {codigo} ja existe!")
            return False
        
        except ValueError:
            novo_livro = Livro(
                codigo=codigo,
                titulo=titulo,
                autor=autor,
                ano_publicacao=ano_publicacao
            )
            self.estoque.append(novo_livro)
            print(f"Livro '{titulo}' cadastrado com sucesso!")
            return True

    def listar(self) -> None:
        if not self.estoque:
            print("Nenhum livro cadastrado!")
            return
        
        print("\nLIVROS CADASTRADOS:")
        print("-" * 50)
        for livro in self.estoque:
            print(f"  Codigo: {livro.codigo}")
            print(f"  Titulo: {livro.titulo}")
            print(f"  Autor: {livro.autor}")
            print(f"  Ano: {livro.ano_publicacao}")
            print(f"  Status: {livro.status}")
            print("-" * 50)

    def emprestar(self, codigo: int) -> None:
        try:
            livro = self.consultar_por_id(codigo=codigo)

            if livro.emprestar():
                print(f"Livro '{livro.titulo}' emprestado com sucesso!")
            else:
                print(f"Livro '{livro.titulo}' nao esta disponivel para emprestimo!")
                
        except ValueError as v:
            print(f"Erro: {v}")

    def devolver(self, codigo: int) -> None:
        try:
            livro = self.consultar_por_id(codigo=codigo)
            
            if livro.devolver():
                print(f"Livro '{livro.titulo}' devolvido com sucesso!")
            else:
                print(f"Livro '{livro.titulo}' ja esta disponivel!")
                
        except ValueError as v:
            print(f"Erro: {v}")

    def excluir(self, codigo: int) -> None:
        try:
            livro = self.consultar_por_id(codigo=codigo)
            
            if livro.status == "Emprestado":
                print(f"Nao e possivel excluir o livro '{livro.titulo}' pois esta emprestado!")
                return
            
            self.estoque.remove(livro)
            print(f"Livro '{livro.titulo}' (codigo {codigo}) excluido com sucesso!")
            
        except ValueError as v:
            print(f"Erro: {v}")

    def sair(self) -> None:
        print("Ate logo!")

    def gestao_livros(self) -> None:
        while True:
            print("\n" + "=" * 40)
            print("SISTEMA DE GESTAO DE LIVROS")
            print("=" * 40)
            print("1 - Cadastrar")
            print("2 - Consultar")
            print("3 - Listar")
            print("4 - Emprestar")
            print("5 - Devolver")
            print("6 - Excluir")
            print("7 - Sair")
            print("=" * 40)

            opcao = input("Opcao: ").strip()

            if opcao == "7":
                self.sair()
                break

            metodo = self.opcoes.get(opcao)

            if not metodo:
                print("Opcao invalida!")
                input("\nPressione Enter para continuar...")
                continue

            if opcao == "1":
                try:
                    codigo = int(input("Codigo: "))
                    titulo = input("Titulo: ")
                    autor = input("Autor: ")
                    ano = int(input("Ano de publicacao: "))
                    metodo(codigo, titulo, autor, ano)
                except ValueError:
                    print("Dados invalidos! Certifique-se de digitar numeros para codigo e ano.")

            elif opcao in ["2", "4", "5", "6"]:
                try:
                    codigo_livro = int(input("Codigo do livro: "))
                    metodo(codigo_livro)
                except ValueError as v:
                    print(f"{v}")

            elif opcao == "3":
                metodo()

            input("\nPressione Enter para continuar...")