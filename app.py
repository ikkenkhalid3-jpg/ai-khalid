"""
Marjane Learning Assistant
A small Streamlit chatbot powered by the Groq API.
Knowledge and instructions are loaded from Marjane-knowledge.json.
"""

import json
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_FILE = BASE_DIR / "Marjane-knowledge.json"

# Load environment variables from the local .env file.
load_dotenv(BASE_DIR / ".env")

st.set_page_config(page_title="Marjane Learning Assistant", page_icon="🛒")
st.title("🛒 Marjane Learning Assistant")
st.caption("Unofficial educational prototype — not affiliated with Marjane.")

@st.cache_data
def load_knowledge():
    """Load the JSON knowledge base and validate that it can be parsed."""
    with KNOWLEDGE_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)

try:
    data = load_knowledge()
except (OSError, json.JSONDecodeError) as exc:
    st.error(f"Could not load Marjane-knowledge.json: {exc}")
    st.stop()

assistant_info = data.get("assistant", {})
instructions = data.get("system_instructions", [])
knowledge_records = data.get("knowledge", [])
faq_records = data.get("faq", [])
limitations = data.get("limitations", [])
sources = data.get("sources", [])

# Build a compact context from the JSON file so answers stay grounded in it.
knowledge_context = {
    "company": data.get("company", {}),
    "knowledge": knowledge_records,
    "faq": faq_records,
    "limitations": limitations,
    "sources": sources,
}
system_prompt = f"""
You are {assistant_info.get('name', 'Marjane Learning Assistant')}.
Role: {assistant_info.get('role', 'Answer questions about Marjane')}.
Personality: {assistant_info.get('tone', 'Clear, welcoming, concise and honest')}.
Instructions from the JSON knowledge file:
{json.dumps(instructions, ensure_ascii=False, indent=2)}

Use ONLY the JSON knowledge context below for facts about Marjane. Do not invent facts,
prices, promotions, stock, delivery fees, opening hours, policies, or account details.
If the file does not answer a question, say the information is not available in this
static knowledge file and direct the user to the official website or relevant source.
For records marked dated_snapshot, clearly say the information was listed in a snapshot
researched on the date in the record and advise checking current terms. For
indexed_reference, say the current page was not freshly verified.
Answer in English unless the user asks in another language. Be concise.
Knowledge context:
{json.dumps(knowledge_context, ensure_ascii=False)}
"""

# Keep conversation history for the current Streamlit session only.
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I can answer questions using the Marjane knowledge file. What would you like to know?",
        }
    ]

with st.sidebar:
    st.subheader("Conversation")
    st.write("Your chat history is kept for this browser session only.")
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Conversation cleared. What would you like to know about Marjane?",
            }
        ]
        st.rerun()

# Display the conversation.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept a new question.
user_prompt = st.chat_input("Ask a question about Marjane...")
if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key or api_key == "your_groq_api_key_here":
        answer = (
            "Please add your Groq API key to the `.env` file as "
            "`GROQ_API_KEY=your_actual_key`, then restart the app. "
            "Get a key at https://console.groq.com/keys."
        )
        with st.chat_message("assistant"):
            st.warning(answer)
    else:
        try:
            client = Groq(api_key=api_key)
            # Send previous turns so the assistant can answer follow-up questions.
            api_messages = [{"role": "system", "content": system_prompt}]
            api_messages.extend(
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
                if m["role"] in ("user", "assistant")
            )

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=api_messages,
                        temperature=0.2,
                        max_tokens=900,
                    )
                    answer = response.choices[0].message.content or (
                        "Sorry, I couldn't produce an answer. Please try again."
                    )
                    st.markdown(answer)
        except Exception as exc:
            # Show a helpful message without exposing secrets.
            answer = (
                "Sorry, the Groq API request failed. Check your internet connection, "
                "API key, model availability, and Groq account limits, then try again. "
                f"Technical detail: {type(exc).__name__}"
            )
            with st.chat_message("assistant"):
                st.error(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

