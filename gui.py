import customtkinter as ctk
import json
import io
import sys

# JSON 명령어 로드
with open("embedding_examples.json", "r", encoding="utf-8") as f:
    command_db = json.load(f)

# 명령어 처리
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


# 기본 설정
ctk.set_appearance_mode("Light")  # "Dark", "Light", "System"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

# 메인 윈도우
window = ctk.CTk()
window.geometry("500x600")
window.title("AI 시스템 제어 GUI")

# 테마 토글
def toggle_theme():
    current = ctk.get_appearance_mode()
    if current == "Light":
        ctk.set_appearance_mode("Dark")
        theme_button.configure(text="☀️ 라이트 모드")
    else:
        ctk.set_appearance_mode("Light")
        theme_button.configure(text="🌙           다크 모드")

# 상단 프레임
top_frame = ctk.CTkFrame(window, fg_color="transparent")
top_frame.pack(fill="x", pady=(15, 5), padx=15)

label_prompt = ctk.CTkLabel(top_frame, text="명령어 입력:", font=ctk.CTkFont(size=14, weight="bold"))
label_prompt.pack(side="left")

theme_button = ctk.CTkButton(
    top_frame,
    text="🌙           다크 모드",
    width=120,
    height=32,
    corner_radius=10,
    command=toggle_theme
)
theme_button.pack(side="right")

# 사용자 입력창
prompt_input = ctk.CTkTextbox(window, height=70, corner_radius=10)
prompt_input.pack(fill="x", padx=15, pady=5)

# 결과 라벨
label_result = ctk.CTkLabel(window, text="결과:", font=ctk.CTkFont(size=14, weight="bold"))
label_result.pack(anchor="w", padx=15, pady=(10, 0))

# 결과 출력창
result_display = ctk.CTkTextbox(window, height=350, corner_radius=10)
result_display.pack(fill="both", expand=True, padx=15, pady=5)
result_display.configure(state="disabled")

# 실행 함수
def send_prompt(event=None):
    prompt = prompt_input.get("0.0", "end").strip()
    if not prompt:
        return
    code, result = find_and_execute(prompt)
    result_display.configure(state="normal")
    result_display.insert("end", f"🧠 입력: {prompt}\n📣 결과:\n{result}\n{'-'*60}\n\n")
    result_display.see("end")
    result_display.configure(state="disabled")
    prompt_input.delete("0.0", "end")

# 엔터키 실행
prompt_input.bind("<Return>", lambda e: (send_prompt(), "break"))

# 실행
window.mainloop()