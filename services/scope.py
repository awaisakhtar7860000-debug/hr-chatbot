HR_KEYWORDS = [
    # English
    "leave", "salary", "overtime", "attendance", "payroll",
    "holiday", "form", "policy", "law", "rules", "working hours",
    "termination", "resignation", "bonus", "increment", "allowance",
    "gratuity", "eobi", "provident fund", "insurance", "medical",
    "contract", "appointment", "warning", "misconduct", "grievance",

    # Roman Urdu
    "chutti", "tanekhwa", "hazri", "form chahiye", "qanoon",
    "overtime", "salary slip", "payslip", "kaam ke ghante",
    "nokri", "resign", "notice period", "increement", "bata",
    "annual", "casual", "sick", "medical leave", "maafi",
    "rules kya hain", "kitni chutti", "leave balance",
    "tarqi", "promotion", "warning letter", "show cause",
]

OUT_OF_SCOPE_HINTS = [
    "recipe", "cricket", "weather", "mausam", "khana",
    "movie", "film", "gana", "song", "game", "khel",
    "politics", "news", "akhbar", "joke", "latifa",
    "coding", "program", "website", "laptop fix",
]


def is_hr_topic(message: str) -> bool:
    msg = message.lower()

    # Agar clearly out of scope hai
    for word in OUT_OF_SCOPE_HINTS:
        if word in msg:
            return False

    # Agar HR keyword hai
    for word in HR_KEYWORDS:
        if word in msg:
            return True

    # Short greetings allow karo
    greetings = ["hello", "hi", "salam", "assalam", "haan", "okay", "help"]
    for g in greetings:
        if msg.strip().startswith(g):
            return True

    # Default: AI ko decide karne do (benefit of doubt)
    return True
