# Grow Chatbot

First-draft Streamlit chat UI for Grow.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="sk-your-key-here"
streamlit run app.py
```

Or copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and put the key there.

## What’s in this draft

- `app.py` — Streamlit chat page and a placeholder `get_bot_reply()` OpenAI call
- Swap `SYSTEM_PROMPT` or `get_bot_reply()` when you add real bot logic
