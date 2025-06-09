# 🔐 RBAC RAG Chatbot

A secure, department-aware **Retrieval-Augmented Generation (RAG)** chatbot built with **Role-Based Access Control (RBAC)**. This application enables professionals to query internal documents, with access strictly limited to their respective departments.

Developed by **NaveenHashira**, this chatbot ensures secure and relevant access to organizational knowledge.

---

## ✨ Key Features

- 🔐 **RBAC-Enabled Access**: Each user is authenticated via HR records and granted access solely to their department's data.
- 📄 **Multi-Format Document Support**: Processes both Markdown (`.md`) and CSV (`.csv`) files.
- ⚡ **Efficient Retrieval**: Uses **FAISS** for fast similarity search.
- 🧠 **LLM-Powered Responses**: Utilizes `Llama3-8b-8192` hosted on **Groq Cloud** for generating context-aware answers.
- 🌐 **Interactive UI**: Built using **Streamlit** for a seamless web-based experience.
- 🧩 **Modular Design**: Clean Python codebase using LangChain and Pandas.

---

## 🧰 Tech Stack

| Component     | Technology                  |
|---------------|-----------------------------|
| Language      | Python                      |
| Framework     | LangChain                   |
| Interface     | Streamlit                   |
| Data Handling | Pandas                      |
| Vector Store  | FAISS                       |
| LLM Provider  | Llama3-8b-8192 (Groq Cloud) |
| Data Formats  | `.md`, `.csv`               |

---

## 🔐 Role-Based Access Control

- Users are authenticated using HR data (typically a `.csv` file).
- Access is restricted to the department the user belongs to.
- For example, a user from the **Marketing** department cannot query **Finance** or **HR** data.

---

## 📁 Project Structure

```
rbac_rag_chatbot/
│
├── app/                       # Core application logic
│   ├── __init__.py
│   ├── auth.py                # Authentication and RBAC logic
│   ├── chat.py                # Chatbot orchestration
│   ├── document_loader.py     # Load documents from md/csv
│   └── vector_store.py        # FAISS vector database
│
├── data/                      # Input documents (.md, .csv)
│
├── app.py                     # Script to trigger backend
├── streamlit_app.py           # Streamlit-based frontend
├── requirements.txt           # Python dependencies
├── .gitignore
└── README.markdown                  # Project documentation
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/NaveenHashira/rbac_rag_chatbot.git
cd rbac_rag_chatbot
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Add Your Documents

Place your Markdown and CSV files in the `data/` folder. Ensure HR data (with user names and departments) is formatted correctly.

### 4. Run the App

```bash
streamlit run streamlit_app.py
```

---

## 🧪 Sample Use Case

A company-wide chatbot allows different departments to query internal reports:

* Alice (HR) asks about onboarding policy → Gets HR data
* Bob (Finance) asks about quarterly budgets → Gets Finance data
* Charlie (HR) asks about Finance reports → ❌ Access Denied

---

## 📌 Notes

* Ensure your HR `.csv` file includes at least `name` and `department` columns.
* The LLM model (Llama3-8b-8192) runs via **Groq Cloud** – valid credentials/API keys are required.

---

## 🧑‍💻 Author

**NaveenHashira**

---

## 📜 License

This project currently has **no license**. If you plan to use or contribute, please contact the author.

---
