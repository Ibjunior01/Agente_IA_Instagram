
from colorama import Fore
from google import genai
from google.genai import types

from app.config import (
    GEMINI_API_KEY,
    GEMINI_MAX_OUTPUT_TOKENS,
    GEMINI_MODEL,
    GEMINI_TEMPERATURE,
    GEMINI_TIMEOUT_MS,
)
from app.memory.session_store import session_store
from app.prompts.flow_prompt import SYSTEM_PROMPT

client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(
        timeout=GEMINI_TIMEOUT_MS,
    ),
)


def processar_mensagem(
    user_id: str,
    mensagem_usuario: str,
) -> str:
    """
    Processa uma mensagem do usuário utilizando
    memória isolada e o Google Gemini.
    """

    if not isinstance(user_id, str) or not user_id.strip():
        raise ValueError("user_id é obrigatório")

    user_id = user_id.strip()

    historico, lock_usuario = (
        session_store.obter_sessao(user_id)
    )

    # Evita que duas mensagens simultâneas
    # do mesmo usuário alterem a sessão.
    with lock_usuario:
        mensagem_historico = types.Content(
            role="user",
            parts=[
                types.Part(
                    text=mensagem_usuario
                )
            ],
        )

        historico.append(
            mensagem_historico
        )

        try:
            resposta = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=historico,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=GEMINI_TEMPERATURE,
                    max_output_tokens=GEMINI_MAX_OUTPUT_TOKENS,
                ),
            )

            resposta_texto = resposta.text

            if not resposta_texto:
                raise RuntimeError(
                    "Gemini retornou uma resposta vazia."
                )

            historico.append(
                types.Content(
                    role="model",
                    parts=[
                        types.Part(
                            text=resposta_texto
                        )
                    ],
                )
            )

            session_store.limitar_historico(
                historico
            )

            return resposta_texto

        except Exception as erro:
            # Uma mensagem que não recebeu
            # resposta válida não deve permanecer
            # no histórico da conversa.
            if (
                historico
                and historico[-1]
                is mensagem_historico
            ):
                historico.pop()

            elif mensagem_historico in historico:
                historico.remove(
                    mensagem_historico
                )

            # Não expõe detalhes internos
            # da exceção nos logs nem ao usuário.
            print(
                Fore.RED
                + "\nErro interno no agente: "
                + f"{type(erro).__name__}\n"
            )

            return (
                "Não consegui processar sua mensagem agora. "
                "Tente novamente em alguns instantes."
            )