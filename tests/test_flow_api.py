from app.routes import flow as flow_routes

HEADERS = {
    "X-API-Key": "test_api_key"
}


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "FLOW online"
    }


def test_request_sem_api_key(client):
    response = client.post(
        "/flow",
        json={
            "user_id": "instagram_teste",
            "mensagem": "Olá",
        },
    )

    assert response.status_code == 401
    assert response.get_json() == {
        "erro": "Não autorizado"
    }


def test_api_key_incorreta(client):
    response = client.post(
        "/flow",
        headers={
            "X-API-Key": "chave_incorreta"
        },
        json={
            "user_id": "instagram_teste",
            "mensagem": "Olá",
        },
    )

    assert response.status_code == 401
    assert response.get_json() == {
        "erro": "Não autorizado"
    }


def test_json_ausente(client):
    response = client.post(
        "/flow",
        headers=HEADERS,
    )

    assert response.status_code == 415

    assert response.get_json() == {
        "erro": "Content-Type deve ser application/json"
    }


def test_json_malformado(client):
    response = client.post(
        "/flow",
        headers=HEADERS,
        content_type="application/json",
        data="{json_invalido",
    )

    assert response.status_code == 400

    assert response.get_json() == {
        "erro": "JSON inválido ou ausente"
    }


def test_user_id_ausente(client):
    response = client.post(
        "/flow",
        headers=HEADERS,
        json={
            "mensagem": "Olá"
        },
    )

    assert response.status_code == 400

    assert response.get_json() == {
        "erro": "user_id é obrigatório"
    }


def test_mensagem_vazia(client):
    response = client.post(
        "/flow",
        headers=HEADERS,
        json={
            "user_id": "instagram_teste",
            "mensagem": "   ",
        },
    )

    assert response.status_code == 400

    assert response.get_json() == {
        "erro": "mensagem não pode ser vazia"
    }


def test_request_valido(client, monkeypatch):
    def processar_mensagem_mock(
        user_id,
        mensagem_usuario,
    ):
        assert user_id == "instagram_teste"

        assert (
            mensagem_usuario
            == "Quero automatizar meu atendimento"
        )

        return "Resposta simulada do agente"

    monkeypatch.setattr(
        flow_routes,
        "processar_mensagem",
        processar_mensagem_mock,
    )

    response = client.post(
        "/flow",
        headers=HEADERS,
        json={
            "user_id": "instagram_teste",
            "mensagem": "Quero automatizar meu atendimento",
        },
    )

    assert response.status_code == 200

    assert response.get_json() == {
        "resposta": "Resposta simulada do agente"
    }


def test_rate_limit_por_usuario(client, monkeypatch):
    def processar_mensagem_mock(
        user_id,
        mensagem_usuario,
    ):
        return "Resposta simulada"

    monkeypatch.setattr(
        flow_routes,
        "processar_mensagem",
        processar_mensagem_mock,
    )

    payload = {
        "user_id": "instagram_rate_limit_teste",
        "mensagem": "Teste de limite",
    }

    # As primeiras 10 requisições devem ser aceitas.
    for _ in range(10):
        response = client.post(
            "/flow",
            headers=HEADERS,
            json=payload,
        )

        assert response.status_code == 200

    # A 11ª requisição do mesmo usuário,
    # dentro da mesma janela, deve ser bloqueada.
    response = client.post(
        "/flow",
        headers=HEADERS,
        json=payload,
    )

    assert response.status_code == 429

    assert response.get_json() == {
        "erro": (
            "Muitas requisições. "
            "Tente novamente em alguns instantes."
        )
    }


def test_mensagem_com_tipo_invalido(client):
    response = client.post(
        "/flow",
        headers=HEADERS,
        json={
            "user_id": "instagram_tipo_mensagem",
            "mensagem": 12345,
        },
    )

    assert response.status_code == 400

    assert response.get_json() == {
        "erro": "mensagem deve ser uma string"
    }


def test_user_id_acima_do_limite(client):
    response = client.post(
        "/flow",
        headers=HEADERS,
        json={
            "user_id": "a" * 129,
            "mensagem": "Teste",
        },
    )

    assert response.status_code == 400

    assert response.get_json() == {
        "erro": (
            "user_id deve possuir no máximo "
            "128 caracteres"
        )
    }


def test_mensagem_acima_do_limite(client):
    response = client.post(
        "/flow",
        headers=HEADERS,
        json={
            "user_id": "instagram_mensagem_grande",
            "mensagem": "a" * 4001,
        },
    )

    assert response.status_code == 400

    assert response.get_json() == {
        "erro": (
            "mensagem deve possuir no máximo "
            "4000 caracteres"
        )
    }