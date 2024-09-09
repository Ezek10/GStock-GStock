import os
import requests

from src.main.exceptions.unauthorized_exception import UnauthorizedException

def get_user_with_token(token: str):
    response = requests.get(
        f"{os.environ['USER_PATH']}/me", 
        headers={"Authorization": f"Bearer {token}"}
    )
    if not response.ok:
        raise UnauthorizedException()
    return response.json()
