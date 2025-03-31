from embedding_store import EmbeddingStore
from prompt_builder import build_prompt
from gpt_interface import ask_gpt
import code_executor
import json

def main():
    store = EmbeddingStore()

    user_input = input("💬 사용자 입력: ")
    result = store.search_and_decide(user_input)

    if result["type"] == "direct":
        code = result["code"]
        print("\n⚡ 직접 실행 코드:\n")
        print(code)
        code_executor.execute_code(code)

    elif result["type"] == "gpt":
        examples = result["examples"]

        if isinstance(examples, str):
            try:
                examples = json.loads(examples)
            except json.JSONDecodeError:
                print("❌ 예시 코드 로드 실패")
                return

        prompt = build_prompt(user_input, examples)
        code = ask_gpt(prompt)
        print("\n🤖 GPT가 생성한 코드:\n")
        print(code)
        code_executor.execute_code(code)

if __name__ == "__main__":
    main()
