import os

from supabase import create_client, Client


def get_supabase_client() -> Client:

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise RuntimeError(
            "Supabase environment variables missing"
        )

    return create_client(
        url,
        key
    )