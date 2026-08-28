import os

import pytest

# Credenciais exclusivamente para testes.
# Devem existir antes da importação da aplicação.
os.environ["API_KEY"] = "test_api_key"
os.environ["GEMINI_API_KEY"] = "test_gemini_key"

from app import create_app  # noqa: E402


@pytest.fixture
def client():
    app = create_app()

    app.config.update(
        TESTING=True,
    )

    with app.test_client() as test_client:
        yield test_client