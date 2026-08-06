from fastapi import APIRouter
from fastapi.responses import JSONResponse

from config.supabase_client import get_supabase_client


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/signup",
    status_code=201,
)
def signup(body: dict):

    email = body.get("email")
    password = body.get("password")


    if not email or not password:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Email and password are required"
            },
        )


    supabase = get_supabase_client()


    response = supabase.auth.sign_up(
        {
            "email": email,
            "password": password,
        }
    )


    if response.user is None:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Signup failed"
            },
        )


    return {
        "user": response.user
    }



@router.post(
    "/login",
)
def login(body: dict):

    email = body.get("email")
    password = body.get("password")


    if not email or not password:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Email and password are required"
            },
        )


    supabase = get_supabase_client()


    response = supabase.auth.sign_in_with_password(
        {
            "email": email,
            "password": password,
        }
    )


    if response.session is None:
        return JSONResponse(
            status_code=401,
            content={
                "error": "Invalid login credentials"
            },
        )


    return {
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token,
    }


@router.post("/logout")
def logout():

    supabase = get_supabase_client()

    try:
        supabase.auth.sign_out()

        return {
            "message": "Successfully logged out"
        }

    except Exception:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Logout failed"
            },
        )