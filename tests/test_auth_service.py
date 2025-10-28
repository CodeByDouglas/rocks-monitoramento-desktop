import pytest
from api.auth_service import AuthService
from api.api_client import APIResponse


class DummyAPIClient:
    def __init__(self):
        self.received_config = None
        self.token = None

    def update_machine_config(self, config_data, auth_token=None):
        self.received_config = config_data
        return APIResponse(True, data={"ok": True})

    def set_auth_token(self, token):
        self.token = token


@pytest.fixture
def auth_service(tmp_path):
    client = DummyAPIClient()
    state_file = tmp_path / "auth_state.json"
    service = AuthService(api_client=client, auth_state_file=str(state_file))
    service._auth_token = "token"  # garantir autenticação
    service._machine_type = "server"
    service._machine_info = {
        "hostname": "test-host",
        "mac_address": "00:11:22:33:44:55",
        "operating_system": "TestOS",
    }
    return service


def test_update_machine_config_builds_expected_payload(auth_service):
    config = {
        "machine_name": "Test Machine",
        "notifications": True,
        "update_frequency": 5,
        "start_with_os": True,
        "monitored_status": {
            "disco": True,
            "rede": False,
            "ram": True,
            "temperatura": False,
            "processos": True,
            "cpu": False,
        },
    }

    response = auth_service.update_machine_config(config)

    expected_payload = {
        "data": {
            "Nome": "Test Machine",
            "MAC": "00:11:22:33:44:55",
            "type": "server",
            "Notificar": True,
            "Frequency": 5,
            "iniciarSO": True,
            "status": {
                "DISCO": True,
                "REDE": False,
                "RAM": True,
                "TEMPERATURA": False,
                "PROCESSO": True,
                "CPU": False,
            },
        }
    }

    assert auth_service.api_client.received_config == expected_payload
    assert response.success is True


def test_update_machine_config_requires_authentication(tmp_path):
    state_file = tmp_path / "auth_state.json"
    service = AuthService(api_client=DummyAPIClient(), auth_state_file=str(state_file))
    service._machine_info = {
        "hostname": "test-host",
        "mac_address": "00:11:22:33:44:55",
        "operating_system": "TestOS",
    }

    response = service.update_machine_config({})

    assert response.success is False
    assert response.error == "Usuário não autenticado"


def test_auth_state_persists_between_instances(tmp_path):
    state_file = tmp_path / "auth_state.json"

    first_client = DummyAPIClient()
    first_service = AuthService(api_client=first_client, auth_state_file=str(state_file))
    first_service._auth_token = "persisted-token"
    first_service._machine_type = "server"
    first_service._machine_info = {
        "hostname": "test-host",
        "mac_address": "00:11:22:33:44:55",
        "operating_system": "TestOS",
    }
    first_service._persist_state()

    second_service = AuthService(api_client=DummyAPIClient(), auth_state_file=str(state_file))

    assert second_service.get_auth_token() == "persisted-token"
    assert second_service.get_machine_type() == "server"
    assert second_service.get_machine_info()["hostname"] == "test-host"
