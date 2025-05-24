from embedding_store import EmbeddingStore
from prompt_builder import build_prompt
from gpt_interface import ask_gpt
import code_executor
import json

def main():
    store = EmbeddingStore()

    while True:
        user_input = input("\n💬 사용자 입력 (종료: quit): ").strip()
        if user_input.lower() in ("quit", "exit"):
            print("프로그램 종료합니다.")
            break

        result = store.search_and_decide(user_input)

        if result["type"] == "direct":
            print(f"\n✅ 명령어 설명:\n{result.get('description', '정확한 명령어입니다.')}")
            code_executor.execute_code(result["code"])

        elif result["type"] == "confirm":
            print(f"\n⚠️ 유사도 {result['similarity']:.2f} 의 명령어가 발견되었습니다: '{result['matched_input']}'")
            print(f"설명: {result.get('description', '유사한 명령어입니다.')}\n")
            confirm = input("이 코드를 실행하시겠습니까? (y/n): ").strip().lower()
            if confirm == "y":
                code_executor.execute_code(result["code"])
            else:
                print("실행 취소됨.")

        elif result["type"] == "gpt":
            examples = result["examples"]
            prompt = build_prompt(user_input, examples)
            code = ask_gpt(prompt)
            print("\n🤖 GPT가 생성한 코드입니다.")
            print("설명: 이 코드는 요청하신 작업을 수행합니다.")
            print("code")
            confirm = input("이 코드를 실행하시겠습니까? (y/n): ").strip().lower()
            if confirm == "y":
                code_executor.execute_code(code)
            else:
                print("실행 취소됨.")

if __name__ == "__main__":
    main()
