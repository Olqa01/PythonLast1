import pytest
import requests
import yaml


@pytest.fixture(scope='session')
def login(request):
    # Чтение конфигурации из файла
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    # Выполнение запроса на авторизацию
    url = 'https://test-stand.gb.ru/gateway/login'
    data = {'username': config['username'], 'password': config['password']}
    response = requests.post(url, data=data)

    # Проверка статуса ответа и наличия токена в ответе
    assert response.status_code == 200
    assert 'token' in response.json()

    # Возвращение токена авторизации
    return response.json()['token']


@pytest.mark.parametrize('owner', ['notMe'])
def test_check_post(owner, login):
    # Выполнение запроса на получение списка постов
    url = 'https://test-stand.gb.ru/api/posts'
    headers = {'X-Auth-Token': login}
    params = {'owner': owner}
    response = requests.get(url, headers=headers, params=params)

    # Проверка статуса ответа и наличия постов в ответе
    assert response.status_code == 200
    assert response.json() != []

    import pytest
    import requests
    import yaml
    import time

    @pytest.fixture(scope='session')
    def login(request):
        # Чтение конфигурации из файла
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)

        # Выполнение запроса на авторизацию
        url = 'https://test-stand.gb.ru/gateway/login'
        data = {'username': config['username'], 'password': config['password']}
        response = requests.post(url, data=data)

        # Проверка статуса ответа и наличия токена в ответе
        assert response.status_code == 200
        assert 'token' in response.json()

        # Возвращение токена авторизации
        return response.json()['token']

    def test_create_post(login):
        # Выполнение запроса на создание поста
        url = 'https://test-stand.gb.ru/api/posts'
        headers = {'X-Auth-Token': login}
        data = {'title': 'Test Post', 'description': 'This is a test post', 'content': 'Lorem ipsum dolor sit amet'}
        response = requests.post(url, headers=headers, data=data)

        # Проверка статуса ответа и наличия созданного поста на сервере
        assert response.status_code == 201

        # Добавление ожидания для обновления списка постов на сервере
        time.sleep(1)

        # Выполнение запроса на получение списка постов
        response = requests.get(url, headers=headers)

        # Проверка статуса ответа и наличия созданного поста в ответе
        assert response.status_code == 200
        assert 'Test Post' in [post['title'] for post in response.json()]

