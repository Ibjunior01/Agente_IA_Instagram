# ============================================================
# FLOWCORE_IA — AGENTE FLOW
# Interface de terminal e camada de compatibilidade
# ============================================================

from colorama import Fore, Style, init

from app.services.agent_service import processar_mensagem

init(autoreset=True)


# ============================================================
# CAMADA DE COMPATIBILIDADE
# ============================================================

def agente_flowcore(
    user_id: str,
    mensagem_usuario: str,
) -> str:
    """
    Encaminha a mensagem para o serviço principal do agente.

    Mantida temporariamente para preservar compatibilidade
    com a API e com a interface de terminal.
    """
    return processar_mensagem(
        user_id=user_id,
        mensagem_usuario=mensagem_usuario,
    )


# ============================================================
# INTERFACE DE TERMINAL
# ============================================================

def iniciar_chat():
    print(Fore.CYAN + "=" * 55)
    print(Fore.CYAN + "   FLOWCORE_IA — AGENTE FLOW ATIVO")
    print(Fore.CYAN + "   Modelo: Gemini 2.5 Flash")
    print(Fore.CYAN + "   Digite 'sair' para encerrar")
    print(Fore.CYAN + "=" * 55)
    print()

    while True:
        try:
            entrada = input(
                Fore.GREEN + "Você: " + Style.RESET_ALL
            ).strip()

            if not entrada:
                continue

            if entrada.lower() in {"sair", "exit", "quit"}:
                print(
                    Fore.CYAN
                    + "\nFLOW: Até logo! Qualquer dúvida, "
                    + "estou aqui. 🚀\n"
                )
                break

            print(
                Fore.YELLOW
                + "\nFLOW processando...\n"
            )

            resposta = agente_flowcore(
                user_id="terminal_local",
                mensagem_usuario=entrada,
            )

            print(
                Fore.CYAN
                + "FLOW: "
                + Style.RESET_ALL
                + resposta
            )
            print()

        except KeyboardInterrupt:
            print(
                Fore.RED
                + "\n\nSessão encerrada.\n"
            )
            break


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    iniciar_chat()