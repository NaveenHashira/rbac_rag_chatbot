import streamlit as st
import os
from dotenv import load_dotenv 
from app.auth import verify_user
from app.vector_store import VectorStoreManager
from app.chat import setup_rag_chain, handle_query

load_dotenv() 

# Path configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HR_DATA_PATH = os.path.join(BASE_DIR, "data","hr","hr_data.csv")

# Initialize session state
def init_session_state():
    keys = {
        "authenticated": False,
        "department": None,
        "vectorstore": None,
        "rag_chain": None,
        "messages": []
    }
    for key, value in keys.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Authentication screen
def auth_screen():
    st.title("🔐 Departmental Knowledge Assistant")
    with st.form("auth_form"):
        name = st.text_input("Full Name", placeholder="Naveen")
        department = st.text_input("Department", placeholder="HR, Finance, Marketing").strip()
        
        if st.form_submit_button("Authenticate"):
            if not name or not department:
                st.error("Please provide both name and department")
                return
                
            if verify_user(HR_DATA_PATH, name, department):
                st.session_state.authenticated = True
                st.session_state.department = department
                st.rerun()
            else:
                st.error("❌ Access denied. You are not registered in that department.")

# Chat interface
def chat_interface():
    st.title(f"💬 {st.session_state.department} Department Assistant")
    
    # Initialize vector store manager
    vector_manager = VectorStoreManager()
    
    # Load vector store if not loaded
    if st.session_state.vectorstore is None:
        with st.spinner("🔍 Loading department knowledge base..."):
            st.session_state.vectorstore = vector_manager.get_department_vectorstore(
                st.session_state.department
            )
            
            if st.session_state.vectorstore is None:
                st.error(f"❌ No documents available for department: {st.session_state.department}")
                st.stop()
            
            api_key = os.getenv("GROQ_API_KEY") 

            if not api_key:
                st.error("❌ GROQ_API_KEY not found in environment variables. Please set it in your .env file.")
                st.stop()

            # Set up RAG chain
            st.session_state.rag_chain = setup_rag_chain(
                st.session_state.vectorstore,
                api_key
            )
    
    # Display chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # Handle user input
    if prompt := st.chat_input(f"Ask about {st.session_state.department} department"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get and display response
        with st.chat_message("assistant"):
            with st.spinner("💭 Thinking..."):
                try:
                    response = handle_query(st.session_state.rag_chain, prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")

# Main app
def main():
    st.set_page_config(
        page_title="Departmental Knowledge Assistant",
        page_icon="🤖",
        layout="centered"
    )
    
    init_session_state()
    
    if not st.session_state.authenticated:
        auth_screen()
    else:
        chat_interface()

if __name__ == "__main__":
    main()