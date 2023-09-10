import json
import requests
from db_connection import db


def is_system_token(token: str) -> (bool, str):
    sql = "SELECT note FROM token WHERE token = '%s' LIMIT 1" % token
    result = db.fetch_one(sql)
    if result is None:
        return False, None
    else:
        return True, result[0]


def is_admin(token: str) -> (bool, str):
    if token is None:
        return False, None
    if token.startswith("X-API-KEY "):
        return is_system_token(token.replace("X-API-KEY ", ""))
    url = "https://homa.snapgenshin.com/Passport/UserInfo"
    headers = {
        "Authorization": token
    }
    response = json.loads(requests.get(url, headers=headers).content.decode('utf-8'))
    try:
        if response["retcode"] == 50031:
            return False, None
        if response["data"]["IsMaintainer"]:
            return True, response["data"]["NormalizedUserName"]
    except KeyError:
        return False, None
