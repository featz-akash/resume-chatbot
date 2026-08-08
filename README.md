# 🤖 Resume AI Assistant

A Resume AI Assistant that allows users to upload their resume in PDF format and ask questions about it using Generative AI and Retrieval-Augmented Generation (RAG).

## 🚀 Features

- 📄 Upload a resume in PDF format
- 🔍 Extract text from the uploaded resume
- 🧠 Create a FAISS vector store for semantic search
- 🔎 Retrieve relevant resume information using similarity search
- 🤖 Generate answers using Google Gemini
- 💬 Ask questions about skills, education, projects, certifications, and experience
- 🎨 Warm, responsive Streamlit user interface
- 🔐 API keys are stored securely using environment variables

## 🛠️ Technologies Used

- **Python**
- **Streamlit**
- **Google Gemini API**
- **LangChain**
- **FAISS**
- **PyMuPDF / PyMuPDF4LLM**
- **python-dotenv**

## 🧠 How It Works

```text
                    Resume PDF
                        │
                        ▼
                 PDF Text Extraction
                        │
                        ▼
                  Text Processing
                        │
                        ▼
                 FAISS Vector Store
                        │
                        ▼
                  User Question
                        │
                        ▼
              Similarity Search (RAG)
                        │
                        ▼
               Relevant Resume Data
                        │
                        ▼
                  Google Gemini
                        │
                        ▼
                    AI Answer

resume-chatbot/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── styles/
│   └── style.css
│
├── utils/
│   ├── llm.py
│   ├── pdf_reader.py
│   ├── vector_store.py
│   └── import_google.py
│
└── uploads/


