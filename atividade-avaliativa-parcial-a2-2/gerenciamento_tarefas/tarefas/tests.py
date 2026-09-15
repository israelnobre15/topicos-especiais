from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Tarefa


class CriarTarefaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = User.objects.create_user(
            username="ana@teste.com", email="ana@teste.com",
            password="senhaforte123", first_name="Ana",
        )
        cls.colega = User.objects.create_user(
            username="bruno@teste.com", email="bruno@teste.com",
            password="senhaforte123", first_name="Bruno",
        )

    def test_criar_tarefa_autenticado_persiste_no_banco(self):
        self.client.force_login(self.usuario)
        resposta = self.client.post(
            reverse("tarefa_criar"),
            {
                "titulo": "Estudar Django",
                "descricao": "Revisar views e templates",
                "status": Tarefa.Status.PENDENTE,
                "responsavel": "",
            },
        )
        tarefa = Tarefa.objects.get(titulo="Estudar Django")
        self.assertRedirects(resposta, reverse("tarefa_detalhe", args=[tarefa.id]))
        self.assertEqual(tarefa.criador, self.usuario)
        self.assertEqual(tarefa.descricao, "Revisar views e templates")

    def test_criador_e_sempre_o_usuario_logado(self):
        self.client.force_login(self.colega)
        self.client.post(
            reverse("tarefa_criar"),
            {"titulo": "Tarefa do Bruno", "status": Tarefa.Status.PENDENTE, "responsavel": ""},
        )
        tarefa = Tarefa.objects.get(titulo="Tarefa do Bruno")
        self.assertEqual(tarefa.criador, self.colega)
        self.assertNotEqual(tarefa.criador, self.usuario)

    def test_criar_tarefa_com_responsavel_atribuido(self):
        self.client.force_login(self.usuario)
        self.client.post(
            reverse("tarefa_criar"),
            {
                "titulo": "Atribuir ao Bruno",
                "status": Tarefa.Status.PENDENTE,
                "responsavel": self.colega.id,
            },
        )
        tarefa = Tarefa.objects.get(titulo="Atribuir ao Bruno")
        self.assertEqual(tarefa.responsavel, self.colega)

    def test_tarefa_sem_responsavel_fica_nula(self):
        self.client.force_login(self.usuario)
        self.client.post(
            reverse("tarefa_criar"),
            {"titulo": "Sem responsável", "status": Tarefa.Status.PENDENTE, "responsavel": ""},
        )
        self.assertIsNone(Tarefa.objects.get(titulo="Sem responsável").responsavel)

    def test_status_default_e_pendente(self):
        Tarefa.objects.create(titulo="Direto no modelo", criador=self.usuario)
        tarefa = Tarefa.objects.get(titulo="Direto no modelo")
        self.assertEqual(tarefa.status, Tarefa.Status.PENDENTE)

    def test_titulo_obrigatorio(self):
        self.client.force_login(self.usuario)
        resposta = self.client.post(
            reverse("tarefa_criar"),
            {"titulo": "", "status": Tarefa.Status.PENDENTE, "responsavel": ""},
        )
        self.assertEqual(Tarefa.objects.count(), 0)
        self.assertEqual(resposta.status_code, 200)

    def test_anonimo_nao_acessa_formulario_de_criacao(self):
        resposta = self.client.get(reverse("tarefa_criar"))
        self.assertRedirects(resposta, "/auth/login/?next=/tarefas/nova/")


class DetalheTarefaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = User.objects.create_user(
            username="ana@teste.com", email="ana@teste.com",
            password="senhaforte123", first_name="Ana",
        )
        cls.tarefa = Tarefa.objects.create(
            titulo="Ler especificação",
            descricao="Ler a spec do projeto",
            criador=cls.usuario,
        )

    def test_detalhe_acessivel_por_autenticado(self):
        self.client.force_login(self.usuario)
        resposta = self.client.get(reverse("tarefa_detalhe", args=[self.tarefa.id]))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Ler especificação")
        self.assertContains(resposta, "Não atribuída")

    def test_anonimo_no_detalhe_e_redirecionado_ao_login(self):
        resposta = self.client.get(reverse("tarefa_detalhe", args=[self.tarefa.id]))
        self.assertRedirects(
            resposta, f"/auth/login/?next=/tarefas/{self.tarefa.id}/"
        )

    def test_detalhe_de_tarefa_inexistente_retorna_404(self):
        self.client.force_login(self.usuario)
        resposta = self.client.get(reverse("tarefa_detalhe", args=[9999]))
        self.assertEqual(resposta.status_code, 404)


class ListaPessoalTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ana = User.objects.create_user(
            username="ana@teste.com", email="ana@teste.com",
            password="senhaforte123", first_name="Ana",
        )
        cls.bruno = User.objects.create_user(
            username="bruno@teste.com", email="bruno@teste.com",
            password="senhaforte123", first_name="Bruno",
        )
        cls.minha_criada = Tarefa.objects.create(
            titulo="Criada por Ana", criador=cls.ana
        )
        cls.minha_atribuida = Tarefa.objects.create(
            titulo="De Bruno para Ana", criador=cls.bruno, responsavel=cls.ana,
            status=Tarefa.Status.ANDAMENTO,
        )
        cls.de_estraneo = Tarefa.objects.create(
            titulo="Do Bruno mesmo", criador=cls.bruno
        )
        cls.concluida = Tarefa.objects.create(
            titulo="Concluída da Ana", criador=cls.ana,
            status=Tarefa.Status.CONCLUIDA,
        )
        Tarefa.objects.filter(pk=cls.minha_criada.pk).update(
            criado_em=timezone.now() - timedelta(minutes=30)
        )
        Tarefa.objects.filter(pk=cls.minha_atribuida.pk).update(
            criado_em=timezone.now() - timedelta(minutes=10)
        )

    def test_lista_mostra_criadas_por_mim_e_atribuidas_a_mim(self):
        self.client.force_login(self.ana)
        resposta = self.client.get(reverse("lista_tarefas"))
        self.assertContains(resposta, "Criada por Ana")
        self.assertContains(resposta, "De Bruno para Ana")
        self.assertNotContains(resposta, "Do Bruno mesmo")

    def test_filtro_por_status(self):
        self.client.force_login(self.ana)
        resposta = self.client.get(reverse("lista_tarefas"), {"status": "concluida"})
        self.assertContains(resposta, "Concluída da Ana")
        self.assertNotContains(resposta, "Criada por Ana")
        self.assertNotContains(resposta, "Do Bruno mesmo")

    def test_filtro_com_status_invalido_equivalente_a_sem_filtro(self):
        self.client.force_login(self.ana)
        resposta = self.client.get(reverse("lista_tarefas"), {"status": "xyz"})
        self.assertContains(resposta, "Criada por Ana")
        self.assertContains(resposta, "Concluída da Ana")

    def test_ordenacao_mais_recente_primeiro(self):
        self.client.force_login(self.ana)
        resposta = self.client.get(reverse("lista_tarefas"))
        posicao_criada = resposta.content.decode().find("Criada por Ana")
        posicao_atribuida = resposta.content.decode().find("De Bruno para Ana")
        self.assertLess(posicao_atribuida, posicao_criada)

    def test_anonimo_e_redirecionado(self):
        resposta = self.client.get(reverse("lista_tarefas"))
        self.assertRedirects(resposta, "/auth/login/?next=/tarefas/")


class DashboardTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ana = User.objects.create_user(
            username="ana@teste.com", email="ana@teste.com",
            password="senhaforte123", first_name="Ana",
        )
        cls.bruno = User.objects.create_user(
            username="bruno@teste.com", email="bruno@teste.com",
            password="senhaforte123", first_name="Bruno",
        )
        Tarefa.objects.create(titulo="P1", criador=cls.ana)
        Tarefa.objects.create(titulo="P2", criador=cls.bruno)
        Tarefa.objects.create(
            titulo="A1", criador=cls.ana, status=Tarefa.Status.ANDAMENTO
        )
        Tarefa.objects.create(
            titulo="C1", criador=cls.bruno, status=Tarefa.Status.CONCLUIDA
        )

    def test_dashboard_mostra_tarefas_de_todos(self):
        self.client.force_login(self.ana)
        resposta = self.client.get(reverse("dashboard"))
        self.assertContains(resposta, "P1")
        self.assertContains(resposta, "P2")
        self.assertContains(resposta, "A1")
        self.assertContains(resposta, "C1")

    def test_dashboard_exibe_contadores_globais(self):
        self.client.force_login(self.ana)
        resposta = self.client.get(reverse("dashboard"))
        self.assertContains(resposta, "4")
        self.assertContains(resposta, "Pendentes")
        self.assertContains(resposta, "Em andamento")
        self.assertContains(resposta, "Concluídas")

    def test_dashboard_com_filtro_por_status(self):
        self.client.force_login(self.ana)
        resposta = self.client.get(reverse("dashboard"), {"status": "andamento"})
        self.assertContains(resposta, "A1")
        self.assertNotContains(resposta, "P1")
        self.assertNotContains(resposta, "C1")

    def test_raiz_redireciona_ao_dashboard(self):
        resposta = self.client.get("/")
        self.assertRedirects(resposta, "/tarefas/dashboard/", fetch_redirect_response=False)

    def test_anonimo_na_raiz_vai_ao_login(self):
        resposta = self.client.get("/", follow=False)
        resposta2 = self.client.get(resposta.url)
        self.assertRedirects(resposta2, "/auth/login/?next=/tarefas/dashboard/")


class PermissoesTarefaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.criador = User.objects.create_user(
            username="ana@teste.com", email="ana@teste.com",
            password="senhaforte123", first_name="Ana",
        )
        cls.responsavel = User.objects.create_user(
            username="bruno@teste.com", email="bruno@teste.com",
            password="senhaforte123", first_name="Bruno",
        )
        cls.estrano = User.objects.create_user(
            username="carla@teste.com", email="carla@teste.com",
            password="senhaforte123", first_name="Carla",
        )
        cls.tarefa = Tarefa.objects.create(
            titulo="Tarefa da dupla",
            criador=cls.criador,
            responsavel=cls.responsavel,
        )

    def test_criador_edita_tarefa(self):
        self.client.force_login(self.criador)
        resposta = self.client.post(
            reverse("tarefa_editar", args=[self.tarefa.id]),
            {
                "titulo": "Editada pela Ana",
                "status": Tarefa.Status.ANDAMENTO,
                "responsavel": self.responsavel.id,
            },
        )
        self.assertRedirects(resposta, reverse("tarefa_detalhe", args=[self.tarefa.id]))
        self.tarefa.refresh_from_db()
        self.assertEqual(self.tarefa.titulo, "Editada pela Ana")
        self.assertEqual(self.tarefa.status, Tarefa.Status.ANDAMENTO)

    def test_responsavel_tem_mesmos_poderes(self):
        self.client.force_login(self.responsavel)
        resposta = self.client.post(
            reverse("tarefa_editar", args=[self.tarefa.id]),
            {
                "titulo": "Tarefa da dupla",
                "status": Tarefa.Status.CONCLUIDA,
                "responsavel": self.criador.id,
            },
        )
        self.assertEqual(resposta.status_code, 302)
        self.tarefa.refresh_from_db()
        self.assertEqual(self.tarefa.status, Tarefa.Status.CONCLUIDA)
        self.assertEqual(self.tarefa.responsavel, self.criador)

    def test_estranho_recebe_403_ao_editar(self):
        self.client.force_login(self.estrano)
        resposta = self.client.get(reverse("tarefa_editar", args=[self.tarefa.id]))
        self.assertEqual(resposta.status_code, 403)
        resposta = self.client.post(
            reverse("tarefa_editar", args=[self.tarefa.id]),
            {"titulo": "Hackeada", "status": Tarefa.Status.PENDENTE},
        )
        self.assertEqual(resposta.status_code, 403)
        self.tarefa.refresh_from_db()
        self.assertNotEqual(self.tarefa.titulo, "Hackeada")

    def test_estranho_recebe_403_ao_excluir(self):
        self.client.force_login(self.estrano)
        resposta = self.client.get(reverse("tarefa_excluir", args=[self.tarefa.id]))
        self.assertEqual(resposta.status_code, 403)
        resposta = self.client.post(reverse("tarefa_excluir", args=[self.tarefa.id]))
        self.assertEqual(resposta.status_code, 403)
        self.assertTrue(Tarefa.objects.filter(pk=self.tarefa.id).exists())

    def test_criador_exclui_via_post_com_confirmacao(self):
        self.client.force_login(self.criador)
        resposta_get = self.client.get(reverse("tarefa_excluir", args=[self.tarefa.id]))
        self.assertContains(resposta_get, "Tem certeza")
        resposta = self.client.post(reverse("tarefa_excluir", args=[self.tarefa.id]))
        self.assertRedirects(resposta, reverse("dashboard"))
        self.assertFalse(Tarefa.objects.filter(pk=self.tarefa.id).exists())

    def test_responsavel_exclui_via_post(self):
        self.client.force_login(self.responsavel)
        self.client.post(reverse("tarefa_excluir", args=[self.tarefa.id]))
        self.assertFalse(Tarefa.objects.filter(pk=self.tarefa.id).exists())

    def test_detalhe_sem_botoes_para_estranho(self):
        self.client.force_login(self.estrano)
        resposta = self.client.get(reverse("tarefa_detalhe", args=[self.tarefa.id]))
        self.assertNotContains(resposta, "tarefa_editar")
        self.assertNotContains(resposta, "tarefa_excluir")

    def test_detalhe_com_botoes_para_criador(self):
        self.client.force_login(self.criador)
        resposta = self.client.get(reverse("tarefa_detalhe", args=[self.tarefa.id]))
        self.assertContains(resposta, "Editar")
        self.assertContains(resposta, "Excluir")
