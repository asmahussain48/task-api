from fastapi import Depends

from dependencies.auth import get_current_user
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
def protected_profile(
    user = Depends(get_current_user)
):

    return {
        "message": "Protected route accessed",
        "user": {
            "id": user.id,
            "email": user.email,
        },
    }
