from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

DADOS_VALIDOS = {
    "nome": "Ana Teste",
    "email": "ana@teste.com",
    "senha": "senhaforte123",
    "confirmar_senha": "senhaforte123",
}


class CadastroTest(TestCase):
    def test_cadastro_cria_usuario_com_senha_hasheada(self):
        self.client.post(reverse("cadastro"), DADOS_VALIDOS)
        usuario = User.objects.get(username="ana@teste.com")
        self.assertTrue(usuario.check_password("senhaforte123"))
        self.assertNotEqual(usuario.password, "senhaforte123")

    def test_cadastro_mapeia_username_email_e_nome(self):
        self.client.post(reverse("cadastro"), DADOS_VALIDOS)
        usuario = User.objects.get(email="ana@teste.com")
        self.assertEqual(usuario.username, "ana@teste.com")
        self.assertEqual(usuario.first_name, "Ana Teste")

    def test_email_duplicado_e_rejeitado(self):
        User.objects.create_user(
            username="ana@teste.com", email="ana@teste.com",
            password="outrasenha123", first_name="Ana",
        )
        resposta = self.client.post(reverse("cadastro"), DADOS_VALIDOS)
        self.assertEqual(User.objects.count(), 1)
        self.assertContains(resposta, "já está cadastrado")

    def test_senhas_divergentes_sao_rejeitadas(self):
        dados = dict(DADOS_VALIDOS, confirmar_senha="diferente123")
        resposta = self.client.post(reverse("cadastro"), dados)
        self.assertEqual(User.objects.count(), 0)
        self.assertContains(resposta, "As senhas não conferem")

    def test_auto_login_apos_cadastro(self):
        self.client.post(reverse("cadastro"), DADOS_VALIDOS)
        self.assertIn("_auth_user_id", self.client.session)

    def test_cadastro_valido_redireciona_ao_dashboard(self):
        resposta = self.client.post(reverse("cadastro"), DADOS_VALIDOS)
        self.assertRedirects(
            resposta, "/tarefas/dashboard/", fetch_redirect_response=False
        )


class LoginTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = User.objects.create_user(
            username="bruno@teste.com", email="bruno@teste.com",
            password="senhaforte123", first_name="Bruno",
        )

    def test_login_valido_autentica_e_redireciona(self):
        resposta = self.client.post(
            reverse("login"),
            {"email": "bruno@teste.com", "senha": "senhaforte123"},
        )
        self.assertRedirects(
            resposta, "/tarefas/dashboard/", fetch_redirect_response=False
        )
        self.assertIn("_auth_user_id", self.client.session)

    def test_login_invalido_mostra_erro_e_nao_autentica(self):
        resposta = self.client.post(
            reverse("login"),
            {"email": "bruno@teste.com", "senha": "errada"},
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "E-mail ou senha inválidos")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_de_usuario_inexistente_mostra_erro(self):
        resposta = self.client.post(
            reverse("login"),
            {"email": "ninguem@teste.com", "senha": "qualquer"},
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "E-mail ou senha inválidos")


class LogoutTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = User.objects.create_user(
            username="carla@teste.com", email="carla@teste.com",
            password="senhaforte123", first_name="Carla",
        )

    def test_logout_via_post_encerra_sessao(self):
        self.client.force_login(self.usuario)
        resposta = self.client.post(reverse("logout"))
        self.assertRedirects(resposta, "/auth/login/", fetch_redirect_response=False)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout_via_get_nao_e_permitido(self):
        self.client.force_login(self.usuario)
        resposta = self.client.get(reverse("logout"))
        self.assertEqual(resposta.status_code, 405)
