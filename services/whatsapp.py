import os
import requests

WA_API_URL = os.environ.get("WA_API_URL")
WA_TOKEN = os.environ.get("WA_TOKEN")


def send_message(to_number: str, message: str) -> bool:
    """WhatsApp pe plain text message bhejo."""
    try:
        headers = {
            "Authorization": f"Bearer {WA_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "text",
            "text": {
                "body": message
            }
        }

        response = requests.post(
            f"{WA_API_URL}/messages",
            headers=headers,
            json=payload,
            timeout=10
        )

        if response.status_code != 200:
            print(f"WA send failed: {response.status_code} — {response.text}")
            return False

        return True

    except Exception as e:
        print(f"WhatsApp error: {e}")
        return False
