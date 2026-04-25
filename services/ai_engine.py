import os
from openai import OpenAI
from supabase import create_client

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY")
)

SYSTEM_PROMPT = """
Tum ek HR Assistant ho Pakistani company ke liye.

ZARURI QAWAID:
1. SIRF company ki HR policy aur Pakistan Labor Laws ke mutabiq jawab do.
2. Agar jawab tumhare database mein nahi hai, toh kaho: "Yeh cheez mujhe maloom nahi, HR department se poochho: hr@company.com"
3. Hamesha Roman Urdu mein baat karo — seedhi, dosti wali zaban mein.
4. Numbers aur rules clearly batao — confused mat karo.
5. Koi bhi personal राय mat do.
6. Jawab mein emojis bilkul mat use karo.
7. Chhota aur clear jawab do — essay mat likho.

PAKISTAN LABOR LAWS (base knowledge):
- Annual Leave: 14 din (Factories Act 1934, Section 49)
- Casual Leave: 10 din per saal
- Sick Leave: 10 din per saal
- Working Hours: 8 ghante din, 48 ghante hafte
- Overtime: Normal rate ka double (Section 34)
- Minimum Wage: Government notification ke mutabiq
- EOBI: Employer 5%, Employee 1% contribution
- Gratuity: 30 din salary per saal service (5 saal baad)
- Notice Period: 1 mahina (both sides)
- Maternity Leave: 12 hafta (West Pakistan Maternity Benefit Ordinance 1958)
"""


def get_relevant_policies(query: str) -> str:
    """Database se relevant policy content fetch karo."""
    try:
        # Simple keyword search — baad mein embeddings se upgrade kar saktay ho
        result = (
            supabase.table("policies")
            .select("title, content, source")
            .ilike("content", f"%{query[:50]}%")
            .limit(3)
            .execute()
        )

        if not result.data:
            return ""

        context = "\nCOMPANY SPECIFIC POLICIES:\n"
        for p in result.data:
            context += f"\n[{p['title']} - {p['source']}]\n{p['content']}\n"

        return context

    except Exception:
        return ""


def get_ai_answer(user_message: str, employee: dict) -> str:
    """OpenAI se HR-specific jawab lo."""

    # Database se relevant policies fetch karo
    policy_context = get_relevant_policies(user_message)

    # Employee info add karo context mein
    emp_context = (
        f"\nEmployee Info: Naam: {employee['name']}, "
        f"Department: {employee.get('department', 'Unknown')}, "
        f"Employee ID: {employee.get('employee_id', 'N/A')}"
    )

    full_system = SYSTEM_PROMPT + emp_context + policy_context

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Sasta aur fast — gpt-4o bhi use kar saktay ho
            messages=[
                {"role": "system", "content": full_system},
                {"role": "user", "content": user_message}
            ],
            max_tokens=400,
            temperature=0.3,  # Low temperature = consistent, factual jawab
        )

        answer = response.choices[0].message.content.strip()
        return answer

    except Exception as e:
        print(f"OpenAI Error: {e}")
        return (
            "Yaar abhi mujhe kuch technical masla aa gaya. "
            "Thodi dair baad dobara poochho, ya seedha HR se milao: hr@company.com"
        )
