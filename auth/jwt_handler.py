import time
from typing import Dict

import jwt

secret_key = "dinusgfbihoagfdvbsibesvdoaghadsgo;ds1e3j298ht4379rt27g4hq83g7eb8qh0eg9fdIAihuBOIVnp9vpb0ihe=8BR[UWvei'pnBR"


def decode_jwt(token: str) -> dict:
    decoded_jwt = jwt.decode(token.encode(), secret_key)
    return decoded_jwt if decoded_jwt["expires"] >= time.time() else {}


def token_response(token: str, user_id: str):
    return {"access_token": token, "user_id": user_id}


def sign_jwt(user_id: str) -> Dict[str, str]:
    payload = {"user_id": user_id, "expires": time.time() + 2400}
    return token_response(jwt.encode(payload=payload, key=secret_key), user_id)
