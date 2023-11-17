from datetime import datetime, timedelta
from .envs import settings
import jwt


def create_jwt_token(data: dict) -> str:
    now = datetime.utcnow()

    return jwt.encode(
        {
            **data,
            **{
                "exp": now + timedelta(minutes=15),
                "iat": now,
            },
        },
        settings.jwt_secret,
        algorithm="HS256",
    )


def decode_jwt_token(token: str) -> dict:
    try:
        data = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=["HS256"],
        )

    except Exception as e:
        print(e)
        return {}

    return data
