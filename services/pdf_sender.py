import os
import base64
import requests

WA_API_URL = os.environ.get("WA_API_URL")  # 360dialog API URL
WA_TOKEN = os.environ.get("WA_TOKEN")

# Form keywords aur unke files ka mapping
FORM_INTENTS = {
    "annual_leave": {
        "keywords": ["annual leave form", "annual leave", "saalana chutti form", "chutti form"],
        "file": "forms/annual_leave_form.pdf",
        "name": "Annual_Leave_Form.pdf",
        "caption": "Yeh lo Annual Leave Form! Fill karke Line Manager ko de dena."
    },
    "casual_leave": {
        "keywords": ["casual leave form", "casual leave", "casual chutti"],
        "file": "forms/casual_leave_form.pdf",
        "name": "Casual_Leave_Form.pdf",
        "caption": "Casual Leave Form ready hai! Usi din ya pehle din submit karna."
    },
    "sick_leave": {
        "keywords": ["sick leave form", "medical leave form", "bimari ki chutti", "sick"],
        "file": "forms/sick_leave_form.pdf",
        "name": "Medical_Leave_Form.pdf",
        "caption": "Medical Leave Form. 2 din se zyada hai toh doctor certificate bhi lagana!"
    },
    "overtime": {
        "keywords": ["overtime form", "extra ghante form", "ot form"],
        "file": "forms/overtime_form.pdf",
        "name": "Overtime_Form.pdf",
        "caption": "Overtime Form. Manager se sign karwana zaroor!"
    },
    "salary_certificate": {
        "keywords": ["salary certificate", "salary slip", "payslip", "tankhwa certificate"],
        "file": "forms/salary_certificate_request.pdf",
        "name": "Salary_Certificate_Request.pdf",
        "caption": "Salary Certificate Request Form. HR office mein jama karna."
    },
    "resignation": {
        "keywords": ["resignation form", "resign", "nokri chorna", "istifa"],
        "file": "forms/resignation_form.pdf",
        "name": "Resignation_Form.pdf",
        "caption": "Resignation Form. Notice period 1 mahina hota hai."
    },
}


def get_form_for_intent(message: str) -> tuple | None:
    """
    Message mein form ki request detect karo.
    Return: (file_path, filename, caption) ya None
    """
    msg = message.lower()

    for form_key, form_data in FORM_INTENTS.items():
        for keyword in form_data["keywords"]:
            if keyword in msg:
                file_path = form_data["file"]
                if os.path.exists(file_path):
                    return (file_path, form_data["name"], form_data["caption"])
                else:
                    print(f"Form file nahi mili: {file_path}")
                    return None

    return None


def send_pdf(to_number: str, file_path: str, caption: str) -> bool:
    """
    PDF ko directly WhatsApp pe bhejo — link nahi, poori file.
    """
    try:
        with open(file_path, "rb") as f:
            file_data = base64.b64encode(f.read()).decode("utf-8")

        filename = os.path.basename(file_path)

        headers = {
            "Authorization": f"Bearer {WA_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "to": to_number,
            "type": "document",
            "document": {
                "link": None,
                "caption": caption,
                "filename": filename,
                # Base64 data directly bhejo
            }
        }

        # 360dialog media upload endpoint use karo
        # Pehle file upload karo, phir message bhejo
        upload_url = f"{WA_API_URL}/media"
        files = {
            "file": (filename, open(file_path, "rb"), "application/pdf"),
            "messaging_product": (None, "whatsapp")
        }

        upload_resp = requests.post(
            upload_url,
            headers={"Authorization": f"Bearer {WA_TOKEN}"},
            files=files
        )

        if upload_resp.status_code == 200:
            media_id = upload_resp.json().get("id")

            # Ab message mein media_id use karo
            msg_payload = {
                "messaging_product": "whatsapp",
                "to": to_number,
                "type": "document",
                "document": {
                    "id": media_id,
                    "caption": caption,
                    "filename": filename
                }
            }

            msg_resp = requests.post(
                f"{WA_API_URL}/messages",
                headers=headers,
                json=msg_payload
            )

            return msg_resp.status_code == 200

    except Exception as e:
        print(f"PDF send error: {e}")
        return False
