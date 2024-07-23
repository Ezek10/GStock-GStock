import os
import requests

def get_user_with_token(token: str, path: str):
    response = requests.get(
        f"{os.environ['USER_PATH']}/current_user", 
        headers={"Authorization": f"Bearer {token}"}, 
        params={"path": path}
    )
    if response.ok:
        return response.json()
    else:
        return False
