import os
from supabase import create_client

supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY")
)


def verify_employee(phone: str) -> dict | None:
    """
    Phone number database mein check karo.
    Number +92XXXXXXXXXX format mein aana chahiye.
    """
    # Number normalize karo — different formats handle karo
    phone = normalize_phone(phone)

    try:
        result = (
            supabase.table("employees")
            .select("*")
            .eq("phone", phone)
            .eq("active", True)
            .execute()
        )

        if result.data:
            return result.data[0]
        return None

    except Exception as e:
        print(f"DB Error: {e}")
        return None


def normalize_phone(phone: str) -> str:
    """
    Alag alag formats ko standard +92 format mein convert karo.
    Examples:
      03001234567   -> +923001234567
      923001234567  -> +923001234567
      +923001234567 -> +923001234567
    """
    phone = phone.strip().replace(" ", "").replace("-", "")

    if phone.startswith("0"):
        phone = "+92" + phone[1:]
    elif phone.startswith("92") and not phone.startswith("+"):
        phone = "+" + phone
    elif not phone.startswith("+"):
        phone = "+92" + phone

    return phone
