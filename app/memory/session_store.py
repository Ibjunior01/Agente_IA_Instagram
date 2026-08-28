from threading import Lock

MAX_HISTORICO_MENSAGENS = 20


class SessionStore:
    """
    Armazena históricos de conversa isolados por usuário.

    Esta implementação utiliza memória local do processo e é
    adequada para o MVP. Em produção, poderá ser substituída
    por Redis sem alterar a lógica principal do agente.
    """

    def __init__(
        self,
        max_historico_mensagens=MAX_HISTORICO_MENSAGENS,
    ):
        self.max_historico_mensagens = (
            max_historico_mensagens
        )

        self.historicos = {}
        self.locks_usuarios = {}

        self._memoria_lock = Lock()

    def obter_sessao(self, user_id: str):
        """
        Retorna o histórico e o lock exclusivos do usuário.
        """
        with self._memoria_lock:
            historico = self.historicos.setdefault(
                user_id,
                [],
            )

            lock_usuario = self.locks_usuarios.setdefault(
                user_id,
                Lock(),
            )

        return historico, lock_usuario

    def limitar_historico(self, historico):
        """
        Mantém somente as mensagens mais recentes.
        """
        if (
            len(historico)
            > self.max_historico_mensagens
        ):
            del historico[
                :-self.max_historico_mensagens
            ]

    def limpar(self):
        """
        Remove todas as sessões armazenadas.
        Útil principalmente durante testes.
        """
        with self._memoria_lock:
            self.historicos.clear()
            self.locks_usuarios.clear()


session_store = SessionStore()