from fastapi import APIRouter


router = APIRouter(
    tags=["Auth"],
)


@router.get("/public/info")
def public_info():
    return {
        "message": "This is a public endpoint",
        "access": "everyone can access",
    }


@router.get("/protected/profile")
def protected_profile():
    return {
        "message": "This is a protected endpoint",
        "user": "temporary",
    }