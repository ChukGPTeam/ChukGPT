
import tkinter as tk
from tkinter import scrolledtext
import json
import io
import sys

# JSON 파일 로드
with open("embedding_examples.json", "r", encoding="utf-8") as f:
    command_db = json.load(f)

# 명령어 매칭 및 실행 함수
def find_and_execute(prompt):
    for item in command_db:
        if item["input"] == prompt:
            old_stdout = sys.stdout
            redirected_output = sys.stdout = io.StringIO()
            try:
                compiled_code = compile(item["code"], "<string>", "exec")
                exec(compiled_code, globals())
                sys.stdout = old_stdout
                output = redirected_output.getvalue().strip()
                return item["code"], output
            except Exception as e:
                sys.stdout = old_stdout
                return item["code"], f"실행 중 오류 발생: {e}"
    return None, "❌ 해당 명령을 찾을 수 없습니다."
# GUI 생성
window = tk.Tk()
window.title("AI 시스템 제어 GUI")
window.geometry("700x600")

# 프롬프트 입력창
tk.Label(window, text="명령어 입력:").pack(anchor="w", padx=10)
prompt_input = scrolledtext.ScrolledText(window, height=3)
prompt_input.pack(fill="x", padx=10, pady=5)

# 결과 출력창
tk.Label(window, text="결과:").pack(anchor="w", padx=10)
result_display = scrolledtext.ScrolledText(window, height=30, state=tk.DISABLED)
result_display.pack(fill="both", expand=True, padx=10, pady=5)

# 실행 함수
def send_prompt():
    prompt = prompt_input.get("1.0", tk.END).strip()
    code, result = find_and_execute(prompt)
    result_display.config(state=tk.NORMAL)
    result_display.insert(tk.END, f"🧠 입력: {prompt}\n")

    result_display.insert(tk.END, f"📣 결과:\n{result}\n{'-'*50}\n")
    result_display.config(state=tk.DISABLED)
    prompt_input.delete("1.0", tk.END)

# 전송 버튼
send_button = tk.Button(window, text="실행", command=send_prompt)
send_button.pack(pady=10)

window.mainloop()
