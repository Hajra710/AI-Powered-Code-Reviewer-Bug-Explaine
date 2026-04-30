import os
from groq import Groq
import gradio as gr

# 🔑 Set your API key here OR via environment variable
# os.environ["GROQ_API_KEY"] = "your_api_key_here"

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def review_code(user_code):
    if not user_code.strip():
        return "⚠️ Please enter some code!"

    prompt = f"""
You are an expert Python code reviewer and teaching assistant for undergraduate students.

Analyze the given code and respond in the following structured format:

1. 🐞 Bugs & Errors:
- Identify syntax errors, logical mistakes, and potential runtime issues.
- Explain WHY it is wrong in simple student-friendly language.

2. 💡 Explanation:
- Explain what the code is doing step by step (in simple terms).

3. ⚡ Complexity Analysis:
- Time Complexity (Big-O)
- Space Complexity (Big-O)
- Brief explanation

4. 🚀 Optimized Code:
- Provide a cleaner, more efficient version of the code
- Follow best practices (PEP8)

5. 📚 Learning Tips:
- Suggest improvements and concepts the student should learn

Here is the code:
{user_code}
"""

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )

    return response.choices[0].message.content


def analyze(code):
    return review_code(code)


# 🎨 Gradio UI
with gr.Blocks(theme=gr.themes.Soft()) as app:

    gr.Markdown("""
    # 🤖 AI Code Reviewer  
    ### Fix Bugs • Learn Faster • Code Smarter 🚀
    """)

    code_input = gr.Textbox(
        label="💻 Paste Your Python Code",
        lines=15,
        placeholder="Example:\nprint('Hello World')"
    )

    analyze_btn = gr.Button("🔍 Analyze Code")

    output = gr.Markdown(label="📊 AI Feedback")

    analyze_btn.click(
        fn=analyze,
        inputs=code_input,
        outputs=output
    )

# Run app
if __name__ == "__main__":
    app.launch()
