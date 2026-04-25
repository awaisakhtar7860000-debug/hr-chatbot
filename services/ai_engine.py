import os
import google.generativeai as genai
from supabase import create_client

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY")
)

SYSTEM_PROMPT = """Tum ek HR Assistant ho Pakistani company ke liye.

ZARURI QAWAID:
1. SIRF company ki HR policy aur Pakistan Labor Laws ke mutabiq jawab do.
2. Agar jawab nahi pata: "Yeh cheez mujhe maloom nahi, HR se poochho: hr@company.com"
3. Hamesha Roman Urdu mein baat karo — dosti wali zaban mein.
4. Chhota aur clear jawab do.
5. Koi personal raay mat do.

PAKISTAN LABOR LAWS:
- Annual Leave: 14 din (Factories Act 1934)
- Casual Leave: 10 din per saal
- Sick Leave: 10 din per saal
- Working Hours: 8 ghante/din, 48 ghante/hafte
- Overtime: Double rate (Section 34)
- Gratuity: 30 din salary per saal (5 saal baad)
- Notice Period: 1 mahina
- Maternity Leave: 12 hafta"""

def get_relevant_policies(query):
    try:
        result = (
            supabase.table("policies")
            .select("title, content, source")
            .ilike("content", f"%{query[:50]}%")
            .limit(3)
            .execute()
        )
        if not result.data:
            return ""
        context = "\nCOMPANY POLICIES:\n"
        for p in result.data:
            context += f"\n[{p['title']}]\n{p['content']}\n"
        return context
    except:
        return ""

def get_ai_answer(user_message, employee):
    policy_context = get_relevant_policies(user_message)
    emp_info = f"\nEmployee: {employee['name']}, Department: {employee.get('department','')}"
    full_prompt = SYSTEM_PROMPT + emp_info + policy_context + f"\n\nEmployee ka sawaal: {user_message}"
    
    try:
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini Error: {e}")
        return "Yaar abhi kuch masla aa gaya. Thodi dair baad poochho ya hr@company.com pe email karo."
