# ==============================
# AI Code Reviewer & Bug Explainer
# ==============================

import os
import gradio as gr
from groq import Groq

MODEL_NAME = "llama-3.3-70b-versatile"


def get_api_key(ui_key: str = "") -> str:
    """
    Prefer the key typed in the UI.
    Fallback to environment variable.
    """
    ui_key = (ui_key or "").strip()
    env_key = (os.environ.get("GROQ_API_KEY") or "").strip()
    return ui_key if ui_key else env_key


def analyze_code(code, language, beginner_mode, api_key):
    if not code or not code.strip():
        return "⚠️ Please enter some code first."

    key = get_api_key(api_key)

    if not key:
        return (
            "❌ GROQ API key is missing.\n\n"
            "Add it in one of these ways:\n"
            "1. Paste it in the API Key box in the app, or\n"
            "2. Set the GROQ_API_KEY environment variable."
        )

    prompt = f"""
You are an expert programming tutor and code reviewer.

Analyze the following {language} code and provide:

1. 🐞 Bugs (if any)
2. 💡 Explanation (simple and clear{" for a beginner" if beginner_mode else ""})
3. ⚡ Optimized Code
4. 📊 Time & Space Complexity (Big-O)

Rules:
- Use clear headings.
- Be beginner-friendly.
- If there are no bugs, say so clearly.
- Keep the answer practical and easy to understand.

Code:
{code}
"""

    try:
        client = Groq(api_key=key)

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error while calling Groq API:\n\n{str(e)}"


def handle_file(file):
    if file is None:
        return ""

    try:
        path = file.name if hasattr(file, "name") else str(file)

        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    except Exception as e:
        return f"❌ Could not read file: {str(e)}"


# ==============================
# Gradio UI
# ==============================
with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown(
        """
        # 🤖 AI Code Reviewer
        ### Fix bugs. Learn faster. Code smarter 🚀
        """
    )

    with gr.Row():
        with gr.Column():
            api_key_input = gr.Textbox(
                label="🔐 GROQ API Key",
                placeholder="Paste your Groq API key here",
                type="password"
            )

            code_input = gr.Textbox(
                label="💻 Paste Your Code",
                lines=15,
                placeholder="Paste your code here..."
            )

            file_upload = gr.File(label="📂 Or Upload Code File")

            language = gr.Dropdown(
                choices=["Python", "C++", "Java", "JavaScript"],
                label="🌐 Select Language",
                value="Python"
            )

            beginner_mode = gr.Checkbox(
                label="🧑‍🎓 Explain like I'm a beginner",
                value=True
            )

            analyze_btn = gr.Button("🔍 Analyze Code")

        with gr.Column():
            output = gr.Markdown(label="📊 AI Analysis")

    file_upload.change(
        fn=handle_file,
        inputs=file_upload,
        outputs=code_input
    )

    analyze_btn.click(
        fn=analyze_code,
        inputs=[code_input, language, beginner_mode, api_key_input],
        outputs=output
    )

if __name__ == "__main__":
    app.launch(debug=True)
