# Marjane Learning Assistant

A beginner-friendly chatbot built with Python, Streamlit, and the Groq API. It answers questions using `Marjane-knowledge.json` and keeps the conversation in Streamlit session state while the current session is active.

> This is an unofficial educational prototype. It is not affiliated with Marjane.

## 1. Requirements

- Python 3.10 or newer
- Internet connection
- A Groq API key: [Groq API key](https://console.groq.com/keys)

## 2. Install

Open a terminal in this project folder and create a virtual environment:

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3. Configure the API key

Open `.env` and replace the placeholder with your own Groq key:

```dotenv
GROQ_API_KEY=your_actual_groq_api_key
```

Get your key from :[Groq API key](https://console.groq.com/keys). Never share it or commit `.env` to Git. The `.gitignore` file excludes `.env`.

Note: This project uses the Groq API, so the variable is named `GROQ_API_KEY`, not `GEMINI_API_KEY`.

## 4. Run the chatbot

From the project folder, run:

```bash
streamlit run app.py
```

Streamlit will show a local URL, usually `http://localhost:8501`. Open it in your browser.

## 5. Files

- `app.py` — Streamlit chat interface, Groq API call, session memory, error handling, and clear-conversation button.
- `Marjane-knowledge.json` — Personality, instructions, knowledge records, FAQ, limitations, and sources.
- `.env` — Local placeholder for the Groq API key.
- `.gitignore` — Keeps secrets and temporary files out of Git.
- `requirements.txt` — Required Python packages.
- `README.md` — Setup and run instructions.

## Notes

- Chat history is held in `st.session_state`; it is not stored in a database and is not intended as permanent memory.
- The knowledge file is a static snapshot, researched on the dates listed inside it. It does not provide live prices, stock, promotions, account balances, or delivery availability.
- The model name in `app.py` is `openai/gpt-oss-120b`. If Groq retires or changes this model, choose a currently available chat model from the Groq console and update the `model` value.
