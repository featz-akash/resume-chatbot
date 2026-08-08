import streamlit as st

from utils.pdf_reader import read_pdf
from utils.vector_store import create_vector_store
from utils.llm import ask_llm



st.set_page_config(
    page_title="Resume AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)




def load_css():
    with open("styles/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()




if "messages" not in st.session_state:
    st.session_state.messages = []

if "resume_uploaded" not in st.session_state:
    st.session_state.resume_uploaded = False

if "vector_db" not in st.session_state:
    st.session_state.vector_db = None




st.markdown("""
<div class="banner">

<h1> Resume AI Assistant</h1>

<p>
Upload your resume and ask anything using Gemini AI + FAISS + RAG
</p>

</div>
""", unsafe_allow_html=True)




with st.sidebar:

    st.markdown("""
    <div class="glass">
        <h2>📄 Resume</h2>
        <p>Upload your resume below</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "",
        type=["pdf"]
    )

    

    if uploaded_file is not None:

        if st.session_state.vector_db is None:

            with st.spinner("📄 Reading Resume..."):

                text = read_pdf(uploaded_file)

                st.session_state.vector_db = create_vector_store(text)

                st.session_state.resume_uploaded = True

        st.markdown(f"""
        <div class="glass">

        <h3 style="color:#2ECC71;">
        ✅ Resume Uploaded
        </h3>

        <p><b>📄 File:</b> {uploaded_file.name}</p>

        <p><b>📦 Size:</b> {round(uploaded_file.size/1024,1)} KB</p>

        <p style="color:#2ECC71;">
        Ready to chat
        </p>

        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### 🤖 AI Status")

    if st.session_state.resume_uploaded:
        st.success("🟢 Resume Ready")
    else:
        st.error("🔴 No Resume")

    st.success("🟢 Gemini Connected")
    st.success("🟢 FAISS Ready")




if len(st.session_state.messages) == 0:

    st.markdown("""
    <div class="glass">

    <h2>👋 Welcome</h2>

    <p>
    Upload your resume and ask questions like:
    </p>

    <ul>

    <li>💼 What are my skills?</li>

    <li>🎓 Tell me about my education.</li>

    <li>🚀 Explain my projects.</li>

    <li>⭐ Summarize my resume.</li>

    <li>📄 What certifications do I have?</li>

    </ul>

    </div>
    """, unsafe_allow_html=True)




for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])




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

        answer = "📄 Please upload a resume first."

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




st.markdown("---")

st.caption(
    "🤖 Powered by Gemini • FAISS • LangChain • Streamlit • Python"
)