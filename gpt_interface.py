from openai import OpenAI
from config import OPENAI_API_KEY, GPT_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

# GPT 응답에서 코드 블록을 추출하는 함수
def extract_code_block(text):
    if "```python" in text:
        return text.split("```python")[-1].split("```")[0].strip()
    elif "```" in text:
        return text.split("```")[-1].split("```")[0].strip()
    else:
        return text.strip()

def ask_gpt(prompt):
    try:
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": "너는 Python 시스템 제어 어시스턴트야."},
                {"role": "user", "content": prompt}
            ]
        )
        full_text = response.choices[0].message.content.strip()
        return extract_code_block(full_text)

    except Exception as e:
        return f"# GPT 호출 오류: {e}"
