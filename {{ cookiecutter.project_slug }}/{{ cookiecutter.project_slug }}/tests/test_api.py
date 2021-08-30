from unittest import mock

from {{ cookiecutter.project_slug }} import app

client = app.test_client()


def test_404():
    response = client.get('/api/echoes')
    assert response.status_code == 404


@mock.patch('{{ cookiecutter.project_slug }}.commons.get_app_version', return_value='1.0')
def test_healthcheck_readiness(_mocked_version):
    response = client.get('/health-check/readiness')
    assert response.status_code == 200
    assert set(response.json.keys()) == {'ready', 'app_version', 'app_type'}


@mock.patch('{{ cookiecutter.project_slug }}.commons.get_app_version', return_value='1.0')
def test_healthcheck_liveness(_mocked_version):
    response = client.get('/health-check/liveness')
    assert response.status_code == 200
    assert set(response.json.keys()) == {'live', 'version', 'timestamp'}


def test_welcome_when_single_word():
    response = client.get('/welcome/tiago')
    assert response.status_code == 200
    assert response.json == {'message': 'Hello, tiago!'}


def test_welcome_when_more_than_one_word():
    response = client.get('/welcome/green lantern Hal Jordan')
    assert response.status_code == 200
    assert response.json == {'message': 'Hello, green lantern Hal Jordan!'}
