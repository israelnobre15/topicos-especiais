from livros.livro import Livro 
from typing import Dict, Callable, List

class Biblioteca:

    def __init__(self):
        self.estoque: List[Livro] = []

        # Dicionário de opções dos métodos que serão chamados
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
        # Método que realiza a consulta de forma direta na lista
        livro = next((livro for livro in self.estoque if livro.codigo == codigo), None)

        if not livro:
            raise ValueError(f"Livro com codigo {codigo} nao encontrado!")

        return livro

    def consultar(self, codigo: int) -> None:
        # Método acessado pela classe para realizar a visualização dos dados
        try:
            livro = self.consultar_por_id(codigo)
            print(livro.__dict__)
        except ValueError as e:
            print(f"Erro: {e}")

    def cadastrar(self, codigo: int, titulo: str, autor: str, ano_publicacao: int) -> bool:
        #Método que permite o cadastro de um novo livro no sistema
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
        # Método que permite a visualização de todos os livros da lista
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
        # Método responsável por realizar o emprestimo de um livro, chamando a função interna do livro para alteração
        try:
            livro = self.consultar_por_id(codigo=codigo)

            if livro.emprestar():
                print(f"Livro '{livro.titulo}' emprestado com sucesso!")
            else:
                print(f"Livro '{livro.titulo}' nao esta disponivel para emprestimo!")
                
        except ValueError as v:
            print(f"Erro: {v}")

    def devolver(self, codigo: int) -> None:
        # Método responsável por administrar a devolução de um livro
        try:
            livro = self.consultar_por_id(codigo=codigo)
            
            if livro.devolver():
                print(f"Livro '{livro.titulo}' devolvido com sucesso!")
            else:
                print(f"Livro '{livro.titulo}' ja esta disponivel!")
                
        except ValueError as v:
            print(f"Erro: {v}")

    def excluir(self, codigo: int) -> None:
        # Método responsável pela exclusão 
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
        # Método responsável por printar os dados de saida
        print("Ate logo!")

    def gestao_livros(self) -> None:
        # Método que administra quais sera o fluxo de funcionamento do dados, faz a utilização de chamadas por dicionário para evitar parte do acoplamento com condicionais.
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