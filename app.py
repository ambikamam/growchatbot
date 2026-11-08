import os

import streamlit as st

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

SYSTEM_PROMPT = """You are Grow, a friendly career-growth chatbot.
Help the user think through skills, career decisions, and next steps.
Keep answers concise, practical, and conversational.
If you need more context, ask one clarifying question."""


def get_api_key() -> str:
    try:
        key = st.secrets.get("OPENAI_API_KEY", "")
        if key:
            return str(key)
    except Exception:
        pass
    return os.getenv("OPENAI_API_KEY", "").strip()


def get_bot_reply(messages: list[dict]) -> str:
    """First-draft LLM call. Replace this function when you have custom bot logic."""
    if OpenAI is None:
        raise RuntimeError("The openai package is not installed. Run `pip install -r requirements.txt`.")

    api_key = get_api_key()
    if not api_key:
        raise RuntimeError(
            "No OpenAI API key found. Add OPENAI_API_KEY to your environment "
            "or to .streamlit/secrets.toml, then refresh."
        )

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, *messages],
        temperature=0.4,
    )
    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("The model returned an empty reply. Try sending the message again.")
    return content


st.set_page_config(page_title="Grow Chatbot", page_icon="🌱", layout="centered")
st.title("🌱 Grow")
st.caption("First-draft Streamlit chat. Ask anything about your career growth.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can I help you grow today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                reply = get_bot_reply(st.session_state.messages)
            except Exception as exc:
                reply = f"I couldn't complete that request. {exc}"
                st.error(reply)
        if not reply.startswith("I couldn't complete that request."):
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
