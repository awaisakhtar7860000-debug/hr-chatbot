from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

from services.verify import verify_employee
from services.scope import is_hr_topic
from services.ai_engine import get_ai_answer
from services.pdf_sender import send_pdf, get_form_for_intent
from services.whatsapp import send_message

load_dotenv()

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    # 360dialog message format parse karo
    try:
        msg_data = data["messages"][0]
        from_number = msg_data["from"]
        msg_type = msg_data["type"]

        if msg_type == "text":
            user_message = msg_data["text"]["body"].strip()
        else:
            # Image/voice etc ignore karo
            send_message(from_number, "Bhai, sirf text message bhejo. Main images nahi samajh sakta abhi.")
            return jsonify({"status": "ok"})

    except (KeyError, IndexError):
        return jsonify({"status": "ok"})

    # Step 1: Employee verify karo
    employee = verify_employee(from_number)

    if not employee:
        msg = (
            "Assalam o Alaikum!\n\n"
            "Aap kaun hain? Aapka number hamare system mein registered nahi hai.\n\n"
            "Meherbani kar ke HR department se rabta karein:\n"
            "hr@company.com"
        )
        send_message(from_number, msg)
        return jsonify({"status": "ok"})

    # Step 2: Scope check karo
    if not is_hr_topic(user_message):
        msg = (
            f"Bhai {employee['name']}, yeh mera kaam nahi! \n\n"
            "Main sirf HR ke masail mein madad kar sakta hoon jaise:\n"
            "- Chutti / Leave\n"
            "- Salary aur Payroll\n"
            "- Forms aur Documents\n"
            "- Attendance\n"
            "- Pakistan Labor Law\n\n"
            "Koi HR sawaal ho to zaroor poochho!"
        )
        send_message(from_number, msg)
        return jsonify({"status": "ok"})

    # Step 3: Form manga check karo
    form_path = get_form_for_intent(user_message)
    if form_path:
        caption = f"Yeh lo {employee['name']} bhai, aapka form!"
        send_pdf(from_number, form_path, caption)
        return jsonify({"status": "ok"})

    # Step 4: AI se jawab lo
    answer = get_ai_answer(user_message, employee)
    send_message(from_number, answer)

    return jsonify({"status": "ok"})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "running", "bot": "HR Assistant"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
