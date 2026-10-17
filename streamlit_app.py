
import uuid
import streamlit as st

from app.graph.workflow import support_graph

st.set_page_config(
    page_title="AI Customer Support Agent",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 AI Customer Support Agent")
st.caption("Ask us about orders, refunds, FAQs, or complaints.")

# Create a conversation ID for this browser session
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# Store messages for displaying the chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept a new message
if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                config = {
                    "configurable": {
                        "thread_id": st.session_state.thread_id
                    }
                }

                result = support_graph.invoke(
                    {
                        "user_message": prompt,
                        "intent": None,
                        "response": None,
                    },
                    config=config,
                )

                response = result.get("response") or (
                    "Sorry, I couldn't generate a response. "
                    "Please try again."
                )

            except Exception as e:
               st.error(f"Error details: {e}")
               response = (
                "Sorry, something went wrong while processing "
                "your request. Please check the error above."
              )

            st.markdown(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
