from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config.supabase_client import get_supabase_client


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):

    token = credentials.credentials

    supabase = get_supabase_client()

    try:
        response = supabase.auth.get_user(token)

        user = response.user

        if user is None:
            raise Exception()

        return user

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )