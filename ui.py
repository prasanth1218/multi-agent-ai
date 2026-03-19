import os
import json
import hashlib
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from datetime import datetime

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ========== PAGE CONFIG ==========
st.set_page_config(page_title="Multi-Agent AI System", page_icon="🤖", layout="wide")

# ========== FILES ==========
USERS_FILE = "users.json"
HISTORY_FILE = "chat_history.json"

# ========== USER MANAGEMENT ==========
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(email, password, name):
    users = load_users()
    if email in users:
        return False, "❌ Email already registered!"
    users[email] = {
        "name": name,
        "password": hash_password(password),
        "created": datetime.now().strftime("%d %b %Y")
    }
    save_users(users)
    return True, "✅ Account created successfully!"

def login_user(email, password):
    users = load_users()
    if email not in users:
        return False, "❌ Email not found!"
    if users[email]["password"] != hash_password(password):
        return False, "❌ Wrong password!"
    return True, users[email]["name"]

# ========== HISTORY MANAGEMENT ==========
def get_history_file(email):
    safe_email = email.replace("@", "_").replace(".", "_")
    return f"history_{safe_email}.json"

def load_history(email):
    history_file = get_history_file(email)
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            return json.load(f)
    return []

def save_history(email, histories):
    history_file = get_history_file(email)
    with open(history_file, "w") as f:
        json.dump(histories, f, indent=2)

# ========== AGENTS ==========
def qa_agent(messages):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": "You are a helpful AI assistant who answers any question clearly and accurately."}] + messages
    )
    return response.choices[0].message.content

def code_builder_agent(messages):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": "You are an expert Python developer. When given a request, write complete working Python code with comments. Always wrap code in ```python blocks."}] + messages
    )
    return response.choices[0].message.content

def reviewer_agent(code):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an expert code reviewer. Review the given Python code and provide: 1) Overall quality rating out of 10, 2) Any bugs or issues found, 3) Suggestions for improvement, 4) Security concerns if any."},
            {"role": "user", "content": f"Review this code:\n{code}"}
        ]
    )
    return response.choices[0].message.content

def generate_chat_title(messages):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Generate a very short title (maximum 5 words) for this conversation. Return only the title, nothing else."},
            {"role": "user", "content": str(messages[:2])}
        ]
    )
    return response.choices[0].message.content.strip()

# ========== AUTH PAGES ==========
def auth_page():
    st.title("🤖 Multi-Agent AI System")
    st.markdown("---")

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

    with tab1:
        st.markdown("### Welcome Back!")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            email = st.text_input("📧 Email:", placeholder="Enter your email", key="login_email")
            password = st.text_input("🔑 Password:", type="password", placeholder="Enter your password", key="login_password")
            if st.button("🚀 Login", use_container_width=True, key="login_btn"):
                if email and password:
                    success, result = login_user(email, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.current_user = email
                        st.session_state.current_name = result
                        st.session_state.chat_histories = load_history(email)
                        st.success(f"✅ Welcome back, {result}!")
                        st.rerun()
                    else:
                        st.error(result)
                else:
                    st.warning("⚠️ Please fill all fields!")

    with tab2:
        st.markdown("### Create New Account!")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            name = st.text_input("👤 Full Name:", placeholder="Enter your name", key="reg_name")
            email_reg = st.text_input("📧 Email:", placeholder="Enter your email", key="reg_email")
            password_reg = st.text_input("🔑 Password:", type="password", placeholder="Create a password", key="reg_password")
            password_confirm = st.text_input("🔑 Confirm Password:", type="password", placeholder="Confirm your password", key="reg_confirm")
            if st.button("📝 Create Account", use_container_width=True, key="reg_btn"):
                if name and email_reg and password_reg and password_confirm:
                    if password_reg != password_confirm:
                        st.error("❌ Passwords do not match!")
                    elif len(password_reg) < 6:
                        st.error("❌ Password must be at least 6 characters!")
                    else:
                        success, message = register_user(email_reg, password_reg, name)
                        if success:
                            st.success(message)
                            st.info("👉 Please go to Login tab to login!")
                        else:
                            st.error(message)
                else:
                    st.warning("⚠️ Please fill all fields!")

# ========== SESSION STATE ==========
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = ""
if "current_name" not in st.session_state:
    st.session_state.current_name = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = "🔍 Q&A Agent"
if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = []
if "theme" not in st.session_state:
    st.session_state.theme = "🌙 Dark Mode"
if "generated_code" not in st.session_state:
    st.session_state.generated_code = None
if "agent_status" not in st.session_state:
    st.session_state.agent_status = "idle"

# ========== THEME ==========
if st.session_state.theme == "🌙 Dark Mode":
    st.markdown("""
    <style>
    .stApp { background-color: #1e1e1e !important; color: white !important; }
    .stSidebar { background-color: #2d2d2d !important; }
    .stSidebar * { color: white !important; }
    .stChatMessage { background-color: #2d2d2d !important; color: white !important; }
    .stChatMessage * { color: white !important; }
    .stMarkdown { color: white !important; }
    .stMarkdown * { color: white !important; }
    p, h1, h2, h3, h4, h5, h6, span, div, label { color: white !important; }
    .stTextInput input { background-color: #3d3d3d !important; color: white !important; }
    .stRadio label { color: white !important; }
    .stButton button { background-color: #3d3d3d !important; color: white !important; border: 1px solid #555 !important; }
    .stSuccess { background-color: #1a472a !important; color: white !important; }
    .stWarning { background-color: #7a4f00 !important; color: white !important; }
    .stInfo { background-color: #1a3a5c !important; color: white !important; }
    code { color: #00ff00 !important; background-color: #2d2d2d !important; }
    .stDownloadButton button { background-color: #1a472a !important; color: white !important; }
    .stTabs [data-baseweb="tab"] { color: white !important; }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    .stApp { background-color: #ffffff !important; color: black !important; }
    .stSidebar { background-color: #f0f0f0 !important; }
    .stSidebar * { color: black !important; }
    .stChatMessage * { color: black !important; }
    p, h1, h2, h3, h4, h5, h6, span, div, label { color: black !important; }
    .stTextInput input { background-color: #ffffff !important; color: black !important; }
    .stButton button { background-color: #f0f0f0 !important; color: black !important; border: 1px solid #ccc !important; }
    code { color: #0000ff !important; background-color: #f0f0f0 !important; }
    .stDownloadButton button { background-color: #d4edda !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# ========== CHECK LOGIN ==========
if not st.session_state.logged_in:
    auth_page()
    st.stop()

# ========== FUNCTIONS ==========
def save_current_chat():
    if st.session_state.messages:
        title = generate_chat_title(st.session_state.messages)
        timestamp = datetime.now().strftime("%d %b %Y %I:%M %p")
        st.session_state.chat_histories.append({
            "title": title,
            "time": timestamp,
            "messages": st.session_state.messages.copy(),
            "agent": st.session_state.agent
        })
        save_history(st.session_state.current_user, st.session_state.chat_histories)

def start_new_chat():
    save_current_chat()
    st.session_state.messages = []
    st.session_state.generated_code = None

def load_chat(index):
    st.session_state.messages = st.session_state.chat_histories[index]["messages"].copy()
    st.session_state.agent = st.session_state.chat_histories[index]["agent"]

# ========== SIDEBAR ==========
st.sidebar.title("🤖 Multi-Agent AI")
st.sidebar.markdown(f"👤 **{st.session_state.current_name}**")
st.sidebar.markdown(f"📧 {st.session_state.current_user}")

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.current_user = ""
    st.session_state.current_name = ""
    st.session_state.messages = []
    st.session_state.chat_histories = []
    st.rerun()

st.sidebar.markdown("---")

if st.sidebar.button(f"{'☀️ Light Mode' if st.session_state.theme == '🌙 Dark Mode' else '🌙 Dark Mode'}"):
    st.session_state.theme = "☀️ Light Mode" if st.session_state.theme == "🌙 Dark Mode" else "🌙 Dark Mode"
    st.rerun()

st.sidebar.markdown("---")

agent_choice = st.sidebar.radio(
    "Choose Your Agent:",
    ["🔍 Q&A Agent", "💻 Code Builder Agent", "🔍💻 Build + Review Agent"]
)
st.session_state.agent = agent_choice

st.sidebar.markdown("---")

st.sidebar.markdown("### 📊 Agent Status")
if st.session_state.agent_status == "thinking":
    st.sidebar.warning(f"⚡ {agent_choice} is working...")
else:
    st.sidebar.success(f"✅ {agent_choice} is ready!")

st.sidebar.markdown("---")

if st.sidebar.button("➕ New Chat"):
    start_new_chat()
    st.rerun()

st.sidebar.markdown("---")

st.sidebar.markdown("### 🕒 Chat History")
if st.session_state.chat_histories:
    for i, chat in enumerate(reversed(st.session_state.chat_histories)):
        index = len(st.session_state.chat_histories) - 1 - i
        if st.sidebar.button(f"💬 {chat['title']} | {chat['time']}", key=f"chat_{index}"):
            load_chat(index)
            st.rerun()
else:
    st.sidebar.info("No chat history yet!")

st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Clear All History"):
    st.session_state.chat_histories = []
    st.session_state.messages = []
    save_history(st.session_state.current_user, [])
    st.rerun()

# ========== MAIN UI ==========
st.title("🤖 Multi-Agent AI System")
st.markdown(f"**Active Agent:** {agent_choice}")
st.markdown("---")

if st.session_state.generated_code:
    st.download_button(
        label="📥 Download Generated Code",
        data=st.session_state.generated_code,
        file_name="generated_app.py",
        mime="text/plain"
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("💬 Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.agent_status = "thinking"

    with st.chat_message("assistant"):
        with st.spinner(f"⚡ {agent_choice} is working..."):

            if agent_choice == "🔍 Q&A Agent":
                response = qa_agent(st.session_state.messages)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

            elif agent_choice == "💻 Code Builder Agent":
                response = code_builder_agent(st.session_state.messages)
                st.markdown(response)
                if "```python" in response:
                    code = response.split("```python")[1].split("```")[0]
                    st.session_state.generated_code = code
                    with open("generated_app.py", "w") as f:
                        f.write(code)
                    st.success("✅ Code saved! Use download button above to download!")
                st.session_state.messages.append({"role": "assistant", "content": response})

            elif agent_choice == "🔍💻 Build + Review Agent":
                build_response = code_builder_agent(st.session_state.messages)
                st.markdown(build_response)
                if "```python" in build_response:
                    code = build_response.split("```python")[1].split("```")[0]
                    st.session_state.generated_code = code
                    with open("generated_app.py", "w") as f:
                        f.write(code)
                    st.success("✅ Code saved! Now reviewing...")
                    with st.spinner("🔍 Reviewer Agent checking..."):
                        review = reviewer_agent(code)
                    st.markdown("### 🔍 Code Review Report:")
                    st.markdown(review)
                    full_response = build_response + "\n\n### 🔍 Review:\n" + review
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    st.session_state.messages.append({"role": "assistant", "content": build_response})

    st.session_state.agent_status = "idle"
    st.rerun()