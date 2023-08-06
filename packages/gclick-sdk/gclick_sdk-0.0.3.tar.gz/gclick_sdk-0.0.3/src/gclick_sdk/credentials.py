import base64
import base64
import requests

from gclick_sdk.exception import AuthenticationException
from gclick_sdk.gclick import DEFAULT_TIMEOUT_AUTHENTICATION, ENDPOINT_ACCESS_TOKEN


class GClickCredentials:
    """
    Classe destinada ao controle de autenticação com as APIs do GClick.
    """

    sistema: int
    usuario: str
    empresa: int
    _access_token: str
    _token_type: str
    _access_token_expires_in: int
    _access_token_scope: str
    _refresh_token: str

    def __init__(
        self,
        sistema: int,
        usuario: str,
        conta: str,
        senha: str,
        empresa: int,
        client_id: str,
        client_secret: str
    ):
        """
        Construtor padrão. Parâmetros:

        - sistema: Código do sistema informado pelo G-Click (para integração).
        - usuario: Apelido do usuário no sistema parceiro correspondente ao apelido do usuário no G-Click.
        - conta: Conta de acesso do usuário junto ao GClick
        - senha: Senha de acesso do usuário junto ao GClick
        - empresa: Código da empresa parceira provido pelo GClick, para integração.
        - client_id: ID da aplicação cliente cadastrada no servidor de autenticação.
        - client_secret: Chave da aplicação cliente cadastrada no servidor de autenticação.
        """
        self.sistema = sistema
        self.usuario = usuario
        self._conta = conta
        self._senha = senha
        self.empresa = empresa
        self._client_id = client_id
        self._client_secret = client_secret

        self._access_token = None
        self._token_type = None
        self._access_token_expires_in = None
        self._access_token_scope = None
        self._refresh_token = None

        # TODO Refatorar para autenticação inicial (sem guardar conta e senha)

    def get_access_token(self) -> str:
        """
        Retorna um access_token do usuário, já autenticado, para comunicação com as APIs do GClick.

        Exceções:
        - AuthenticationException: Representa qualquer problema de autenticação junto ao servidor de autenticação (a mensagem contém maiores detalhes).
        """
        # TODO Refatorar para controle de validação do access_token e renovação pelo refresh_token

        # Construindo a requisição
        data = {
            'username': self._conta,
            'password': self._senha,
            'grant_type': 'password',
            'empresa': self.empresa
        }

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {self._get_basic_auth(self._client_id, self._client_secret)}'
        }

        # Realizando a requisição
        resp = requests.post(
            ENDPOINT_ACCESS_TOKEN,
            data=data,
            timeout=DEFAULT_TIMEOUT_AUTHENTICATION,
            headers=headers
        )

        # Tratando o resultado
        if resp.status_code != 200:
            raise AuthenticationException(
                f'Erro de autenticação do usuário: {resp.text}')

        json_resp = resp.json()
        self._access_token = json_resp['access_token']
        self._token_type = json_resp['token_type']
        self._access_token_expires_in = json_resp['expires_in']
        self._access_token_scope = json_resp['scope']
        self._refresh_token = json_resp['refresh_token']

        # Retornando o acess_token
        return self._access_token

    def _get_basic_auth(self, client_id: str, client_secret: str):
        """
        Codifica a concatenação "<client_id>:<client_secret>" em base64, para autenticação basica,
        junto ao servidor de autenticação oauth (para recuperar um access_token).

        Parametros:
        - client_id: ID da aplicação cliente cadastrada no servidor de autenticação.
        - client_secret: Chave da aplicação cliente cadastrada no servidor de autenticação.
        """

        basic_credentials = f'{client_id}:{client_secret}'
        basic_credentials = base64.b64encode(
            basic_credentials.encode('utf-8')).decode('utf-8')

        return basic_credentials
