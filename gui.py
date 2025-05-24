import customtkinter as ctk
import json
import io
import sys
from embedding_store import EmbeddingStore
from prompt_builder import build_prompt
from gpt_interface import ask_gpt
import code_executor
from tkinter import messagebox

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

store = EmbeddingStore()

window = ctk.CTk()
window.geometry("600x700")
window.title("AI 시스템 제어 GUI")

def toggle_theme():
    current = ctk.get_appearance_mode()
    if current == "Light":
        ctk.set_appearance_mode("Dark")
        theme_button.configure(text="☀️ 라이트 모드")
    else:
        ctk.set_appearance_mode("Light")
        theme_button.configure(text="🌙 다크 모드")

top_frame = ctk.CTkFrame(window, fg_color="transparent")
top_frame.pack(fill="x", pady=(15, 5), padx=15)

label_prompt = ctk.CTkLabel(top_frame, text="명령어 입력:", font=ctk.CTkFont(size=14, weight="bold"))
label_prompt.pack(side="left")

theme_button = ctk.CTkButton(
    top_frame,
    text="🌙 다크 모드",
    width=120,
    height=32,
    corner_radius=10,
    command=toggle_theme
)
theme_button.pack(side="right")

prompt_input = ctk.CTkTextbox(window, height=70, corner_radius=10)
prompt_input.pack(fill="x", padx=15, pady=5)

label_result = ctk.CTkLabel(window, text="결과:", font=ctk.CTkFont(size=14, weight="bold"))
label_result.pack(anchor="w", padx=15, pady=(10, 0))

result_display = ctk.CTkTextbox(window, height=450, corner_radius=10)
result_display.pack(fill="both", expand=True, padx=15, pady=5)
result_display.configure(state="disabled")

def execute_code_and_capture_output(code):
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        exec(code, globals())
        output = sys.stdout.getvalue()
    except Exception as e:
        output = f"실행 중 오류 발생: {e}"
    finally:
        sys.stdout = old_stdout
    return output.strip()

def process_input(prompt):
    if not prompt:
        return "⚠️ 명령어를 입력해주세요."

    result = store.search_and_decide(prompt)

    if result["type"] == "direct":
        desc = result.get("description", "정확한 명령어입니다.")
        code = result["code"]
        output = execute_code_and_capture_output(code)
        return f"✅ 명령어 설명:\n{desc}\n\n⚡ 직접 실행 코드:\n{code}\n\n📣 출력 결과:\n{output}"

    elif result["type"] == "confirm":
        desc = result.get("description", "유사한 명령어입니다.")
        code = result["code"]
        matched_input = result.get("matched_input", "")
        similarity = result.get("similarity", 0)
        confirm_msg = (
            f"⚠️ 유사도 {similarity:.2f} 의 명령어가 발견되었습니다: '{matched_input}'\n"
            f"설명: {desc}\n\n코드를 실행하시겠습니까?"
        )
        if messagebox.askyesno("명령어 실행 확인", confirm_msg):
            output = execute_code_and_capture_output(code)
            return f"📣 실행 완료\n출력 결과:\n{output}"
        else:
            return "⚠️ 실행이 취소되었습니다."

    elif result["type"] == "gpt":
        examples = result["examples"]
        prompt_for_gpt = build_prompt(prompt, examples)
        code = ask_gpt(prompt_for_gpt)

        confirm_msg = (
            "🤖 GPT가 생성한 코드입니다. 실행하시겠습니까?\n\n"
            "코드 설명: 요청하신 작업을 수행하는 코드입니다.\n\n"
            f"{code}"
        )
        if messagebox.askyesno("GPT 코드 실행 확인", confirm_msg):
            output = execute_code_and_capture_output(code)
            return f"📣 실행 완료\n출력 결과:\n{output}"
        else:
            return "⚠️ 실행이 취소되었습니다."

def send_prompt(event=None):
    prompt = prompt_input.get("0.0", "end").strip()
    if not prompt:
        return
    result_text = process_input(prompt)
    result_display.configure(state="normal")
    result_display.insert("end", f"🧠 입력: {prompt}\n📣 결과:\n{result_text}\n{'-'*60}\n\n")
    result_display.see("end")
    result_display.configure(state="disabled")
    prompt_input.delete("0.0", "end")

prompt_input.bind("<Return>", lambda e: (send_prompt(), "break"))

window.mainloop()
