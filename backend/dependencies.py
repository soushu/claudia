import uuid
from typing import Annotated

from fastapi import Depends
from fastapi_nextauth_jwt import NextAuthJWTv4

JWT = NextAuthJWTv4(
    csrf_prevention_enabled=False,
)


async def get_current_user_id(token: Annotated[dict, Depends(JWT)]) -> uuid.UUID:
    return uuid.UUID(token["id"])
