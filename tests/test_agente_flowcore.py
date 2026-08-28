from app.memory.session_store import session_store
from app.services import agent_service


class FakeResponse:
    def __init__(self, text):
        self.text = text


def _texto_do_historico(contents):
    textos = []

    for content in contents:
        for part in content.parts:
            if part.text:
                textos.append(part.text)

    return " ".join(textos)


def setup_function():
    """
    Garante memória limpa antes de cada teste.
    """
    session_store.limpar()


def test_historico_isolado_entre_usuarios(monkeypatch):
    historicos_enviados_ao_gemini = []

    def generate_content_mock(**kwargs):
        texto_historico = _texto_do_historico(
            kwargs["contents"]
        )

        historicos_enviados_ao_gemini.append(
            texto_historico
        )

        numero_chamada = len(
            historicos_enviados_ao_gemini
        )

        return FakeResponse(
            f"resposta simulada {numero_chamada}"
        )

    monkeypatch.setattr(
        agent_service.client.models,
        "generate_content",
        generate_content_mock,
    )

    resposta_a1 = agent_service.processar_mensagem(
        user_id="instagram_usuario_a",
        mensagem_usuario="SEGREDO_EXCLUSIVO_USUARIO_A",
    )

    resposta_b1 = agent_service.processar_mensagem(
        user_id="instagram_usuario_b",
        mensagem_usuario="Mensagem exclusiva do usuario B",
    )

    resposta_a2 = agent_service.processar_mensagem(
        user_id="instagram_usuario_a",
        mensagem_usuario="Segunda mensagem do usuario A",
    )

    assert resposta_a1 == "resposta simulada 1"
    assert resposta_b1 == "resposta simulada 2"
    assert resposta_a2 == "resposta simulada 3"

    historico_usuario_b = (
        historicos_enviados_ao_gemini[1]
    )

    assert (
        "SEGREDO_EXCLUSIVO_USUARIO_A"
        not in historico_usuario_b
    )

    assert (
        "resposta simulada 1"
        not in historico_usuario_b
    )

    historico_segunda_chamada_a = (
        historicos_enviados_ao_gemini[2]
    )

    assert (
        "SEGREDO_EXCLUSIVO_USUARIO_A"
        in historico_segunda_chamada_a
    )

    assert (
        "resposta simulada 1"
        in historico_segunda_chamada_a
    )

    assert (
        "instagram_usuario_a"
        in session_store.historicos
    )

    assert (
        "instagram_usuario_b"
        in session_store.historicos
    )

    assert (
        session_store.historicos[
            "instagram_usuario_a"
        ]
        is not
        session_store.historicos[
            "instagram_usuario_b"
        ]
    )


def test_falha_gemini_retorna_fallback_seguro(
    monkeypatch,
    capsys,
):
    def generate_content_mock(**kwargs):
        raise RuntimeError(
            "SEGREDO_TECNICO_NAO_PODE_VAZAR"
        )

    monkeypatch.setattr(
        agent_service.client.models,
        "generate_content",
        generate_content_mock,
    )

    resposta = agent_service.processar_mensagem(
        user_id="instagram_erro",
        mensagem_usuario="Mensagem de teste",
    )

    assert resposta == (
        "Não consegui processar sua mensagem agora. "
        "Tente novamente em alguns instantes."
    )

    assert (
        session_store.historicos[
            "instagram_erro"
        ]
        == []
    )

    saida_terminal = capsys.readouterr().out

    assert "RuntimeError" in saida_terminal

    assert (
        "SEGREDO_TECNICO_NAO_PODE_VAZAR"
        not in saida_terminal
    )