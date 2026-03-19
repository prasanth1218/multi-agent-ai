import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ========== AGENT 1 - Q&A Agent ==========
def qa_agent(question):
    print(f"\n🤖 QA Agent thinking...")
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant who answers any question clearly and accurately."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

# ========== AGENT 2 - Code Builder Agent ==========
def code_builder_agent(request):
    print(f"\n💻 Code Builder Agent working...")
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an expert Python developer. When given a request, write complete, working Python code only. No explanations, just clean code with comments."},
            {"role": "user", "content": f"Build this: {request}"}
        ]
    )
    code = response.choices[0].message.content
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0]
    elif "```" in code:
        code = code.split("```")[1].split("```")[0]
    filename = "generated_app.py"
    with open(filename, "w") as f:
        f.write(code)
    print(f"✅ Code saved to {filename}")
    return code, filename

# ========== AGENT 3 - Reviewer Agent ==========
def reviewer_agent(code):
    print(f"\n🔍 Reviewer Agent checking the code...")
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an expert code reviewer. Review the given Python code and provide: 1) Overall quality rating out of 10, 2) Any bugs or issues found, 3) Suggestions for improvement, 4) Security concerns if any."},
            {"role": "user", "content": f"Review this code:\n{code}"}
        ]
    )
    return response.choices[0].message.content

# ========== MAIN SYSTEM ==========
print("=" * 50)
print("🧠 MULTI-AGENT AI SYSTEM")
print("=" * 50)

while True:
    print("\nWhat do you want to do?")
    print("1. Ask a question (Q&A Agent)")
    print("2. Build an app (Code Builder Agent)")
    print("3. Build and Review an app (Agent 2 + Agent 3)")
    print("4. Exit")

    choice = input("\nEnter choice (1/2/3/4): ")

    if choice == "1":
        question = input("\n💬 Ask anything: ")
        answer = qa_agent(question)
        print(f"\n✅ Answer:\n{answer}")
        print("-" * 50)

    elif choice == "2":
        request = input("\n💬 What app do you want to build? ")
        code, filename = code_builder_agent(request)
        print(f"\n✅ Generated Code:\n{code}")
        print(f"\n📁 Saved to: {filename}")
        print("-" * 50)

    elif choice == "3":
        request = input("\n💬 What app do you want to build? ")
        code, filename = code_builder_agent(request)
        print(f"\n✅ Generated Code:\n{code}")
        print(f"\n📁 Saved to: {filename}")
        print("\n" + "=" * 50)
        review = reviewer_agent(code)
        print(f"\n🔍 Code Review Report:\n{review}")
        print("-" * 50)

    elif choice == "4":
        print("👋 Goodbye!")
        break

    else:
        print("❌ Invalid choice! Enter 1, 2, 3 or 4")