def build_prompt(user_input, examples=[]):
    prompt = "너는 컴퓨터 제어용 Python 코드를 작성하는 어시스턴트야.\n"
    prompt += "사용자의 명령을 받으면 실행 가능한 코드를 작성해줘.\n"
    prompt += "설명 없이 **코드만 출력**해.\n\n"
    prompt += "Output은 반드시 ```python 블록 안의 코드만 포함해야 하며, 그 외 텍스트는 절대 출력하지 마.\n"

    for ex in examples:
        prompt += f"Input: {ex['input']}\nOutput:\n{ex['code']}\n\n"

    prompt += f"Input: {user_input}\nOutput:\n"
    return prompt