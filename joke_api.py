import requests
#not my code! Was taken from https://dev.to/alanjc/creating-a-discord-bot-with-python-33f3
URL = 'https://official-joke-api.appspot.com/random_joke'


def check_valid_status_code(request):
    if request.status_code == 200:
        return request.json()

    return False


def get_joke():
    request = requests.get(URL)
    data = check_valid_status_code(request)

    return data