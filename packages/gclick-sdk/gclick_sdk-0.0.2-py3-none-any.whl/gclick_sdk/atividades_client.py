import requests

from gclick_sdk.gclick import DEFAULT_TIMEOUT_UPLOAD, ENDPOINT_ATIVIDADES_RESPOSTA
from gclick_sdk.atividade_exception import AtividadeNotFoundException, BaixadaAnteriormenteException, BaixaUnknowException
from gclick_sdk.credentials import GClickCredentials
from gclick_sdk.exception import UnauthorizedException


class AtividadesClient:
    """
    Client para os endpoints destinados à manipulação de Atividades.
    """

    def __init__(self, credentials: GClickCredentials):
        self._credentials = credentials

    def baixar_upload(
        self,
        id_atividade: str,
        inscricao: str,
        competencia: int,
        file_content: bytes,
        file_name: str,
        file_mimetype: str,
        usuario: str = None
    ):
        """
        Realiza a baixa de atividade realizando o upload de arquivo.

        Parâmetros:
        - id_atividade: ID da atividade.
        - inscricao: Inscrição do cliente do escritório contábil (CPF ou CNPJ).
        - competencia: Data da competência no formato AAAAMM.
        - file_content: Conteúdo, em bytes, do arquivo a sofrer upload.
        - file_name: Nome do arquivo sofrendo upload.
        - file_mimetype: Mimetype do arquivo sofrendo upload.
        - usuario [opcional]: Apelido do usuário no sistema parceiro.

        Obs.: Se o parâmetro "usuario" não for passado, será assumido o usuário recebido com o objeto
        de credenciais (no construtor da classe).
        """
        # TODO Se eu não prover um arquivo para o endpoint de baixa v3, ele faz a baixa sem o arquivo?

        # Resolvendo apelido do usuário
        if usuario is None:
            usuario = self._credentials.usuario

        # Montando corpo da requisição
        data = {
            'idAtividade': id_atividade,
            'inscricao': inscricao,
            'competencia': competencia,
            'usuario': usuario,
            'sistema': self._credentials.sistema
        }

        # Preparando o arquivo para upload
        if (
            file_content is None
            or file_content is None
            or file_mimetype is None
        ):
            raise BaixaUnknowException('File parameter missing')

        files = {
            'arquivo': (file_name, file_content, file_mimetype)
        }

        # Preparando o header de autenticação
        access_token = self._credentials.get_access_token()
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        # Realizando a requisição
        resp = requests.post(ENDPOINT_ATIVIDADES_RESPOSTA,
                             data=data, files=files, timeout=DEFAULT_TIMEOUT_UPLOAD, headers=headers)

        if resp.status_code in [200, 201]:
            return
        elif resp.status_code == 204:
            raise BaixadaAnteriormenteException(resp.text)
        elif resp.status_code == 401:
            raise UnauthorizedException(resp.text)
        elif resp.status_code == 404:
            raise AtividadeNotFoundException(resp.text)
        elif resp.status_code == 400:
            raise BaixaUnknowException(resp.text)
        else:
            resp.raise_for_status()
