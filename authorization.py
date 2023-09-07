import json
import requests


def is_admin(token: str) -> bool:
    url = "https://homa.snapgenshin.com/Passport/UserInfo"
    headers = {
        "Authorization": token
    }
    response = json.loads(requests.get(url, headers=headers).content.decode('utf-8'))
    print(response)
    try:
        if response["retcode"] == 50031:
            return False
        if response["data"]["IsMaintainer"]:
            return True
    except KeyError:
        return False
