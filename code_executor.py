import subprocess   # 외부 프로그램 실행을 위한 모듈
import textwrap     # 텍스트 정렬을 위한 모듈

def execute_code(code, file_path="generated_code.py"):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

    print("\n📄 생성된 코드:\n")
    print(textwrap.indent(code, "    "))

    confirm = input("\n실행할까요? (y/n): ")
    if confirm.lower() == "y":
        result = subprocess.run(["python", file_path], capture_output=True, text=True)
        print("\n🚀 실행 결과:\n", result.stdout or result.stderr)
    else:
        print("🚫 실행 취소됨.")
