import requests

from config import settings
from exceptions import InvalidToken, WrongPassword, NoneConnection


def get_letter(token: str, password: str) -> dict:

    data = {'password': password}
    url = settings.url + f'/letters/get/{token}'

    req = requests.get(url=url, json=data)

    match req.status_code:
        case 404: raise InvalidToken
        case 401: raise WrongPassword

    return req.json()

def create_letter(title: str, password: str,
                  body: str | None, author: str | None) -> str:
    data = {
        'title': title,
        'password': password,
        'body': body,
        'author': author
    }
    url = settings.url + f'/letters/new'

    try:
        req = requests.post(url=url, json=data)

        token = req.json()['token']

        return token
    except:
        raise NoneConnection


if __name__ == "__main__":
    password = '1234'
    token = create_letter("Привет", password, "Привет мир это я", None)
    print(get_letter(token=token, password=password))

