import streamlit as st
from utils.pdf_reader import read_pdf
from utils.vector_store import create_vector_store
from utils.llm import ask_llm

st.set_page_config(
    page_title="Resume Chatbot",
    page_icon="📄",
    layout="wide"
)

# -------------------------
# Session State
# -------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "resume_uploaded" not in st.session_state:
    st.session_state.resume_uploaded = False

if "vector_db" not in st.session_state:
    st.session_state.vector_db = None

# -------------------------
# Title
# -------------------------

st.title("📄 Resume Chatbot")
st.caption("Ask anything about an uploaded resume")

# -------------------------
# Sidebar
# -------------------------

with st.sidebar:

    st.header("Upload Resume")

    uploaded_file = st.file_uploader(
        "Choose PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:

        if st.session_state.vector_db is None:

            with st.spinner("Reading Resume..."):

                text = read_pdf(uploaded_file)

                st.session_state.vector_db = create_vector_store(text)

                st.session_state.resume_uploaded = True

            st.success("Resume Uploaded")

        st.info(uploaded_file.name)

# -------------------------
# Chat History
# -------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------
# Chat Input
# -------------------------

prompt = st.chat_input("Ask about the resume...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    if not st.session_state.resume_uploaded:

        answer = "Please upload a resume first."

    else:

        docs = st.session_state.vector_db.similarity_search(
            prompt,
            k=3
        )

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        answer = ask_llm(
            context,
            prompt
        )   

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )