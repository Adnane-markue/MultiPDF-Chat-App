import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from docx import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory 
import os
from htmlTemplates import css, bot_template, user_template

def get_pdf_text(uploaded_files):
    text = ""
    for uploaded_file in uploaded_files:
        if uploaded_file.type == "application/pdf":
            try:
                reader = PdfReader(uploaded_file)
                for i, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                    else:
                        st.warning(f"Warning: No text extracted from page {i+1} of {uploaded_file.name}")
            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {str(e)}")
    return text

def get_docx_text(uploaded_files):
    text = ""
    for uploaded_file in uploaded_files:
        if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            try:
                doc = Document(uploaded_file)
                for para in doc.paragraphs:
                    if para.text.strip():
                        text += para.text + "\n"
            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {str(e)}")
    return text

def get_text_chunks(text):
    if not text.strip():
        return []
    
    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separator="\n",
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks  

def get_vectorstore(text_chunks):
    if not text_chunks:
        st.error("No text chunks available to create vector store")
        return None
    
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vectorstore = FAISS.from_texts(
            texts=text_chunks,
            embedding=embeddings,
            metadatas=[{"source": f"chunk-{i}"} for i in range(len(text_chunks))]
        )
        return vectorstore
    except Exception as e:
        st.error(f"Error creating vector store: {str(e)}")
        return None

def get_conversational_chain(vectorstore):
    if vectorstore is None:
        return None
    
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            input_key="question",
            output_key="answer"
        )
        
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            memory=memory,
            return_source_documents=True,
            get_chat_history=lambda h: h,
            verbose=False
        )
        
        return conversation_chain
    except Exception as e:
        st.error(f"Error creating conversation chain: {str(e)}")
        return None

def handle_userinput(user_question):
    if not st.session_state.conversation:
        st.warning("Please process documents first")
        return
    
    try:
        response = st.session_state.conversation.invoke({
            "question": user_question,
            "chat_history": st.session_state.get("chat_history", [])
        })
        
        st.session_state.chat_history = response["chat_history"]
        
        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
                
    except Exception as e:
        st.error(f"Error processing your question: {str(e)}")

def main():
    load_dotenv()
    st.set_page_config(page_title="Document Chat App", page_icon=":books:", layout="wide")
    st.write(css, unsafe_allow_html=True)
    
    # Initialize session state
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    st.header("Chat with multiple documents :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)
    
    with st.sidebar:
        st.subheader("Your documents")
        uploaded_files = st.file_uploader(
            "Upload your documents", 
            type=["pdf", "docx"], 
            accept_multiple_files=True
        )
        
        if st.button("Process Documents"):
            with st.spinner("Processing..."):
                # Process documents
                pdf_text = get_pdf_text(uploaded_files)
                docx_text = get_docx_text(uploaded_files)
                combined_text = pdf_text + "\n" + docx_text
                
                if not combined_text.strip():
                    st.error("No text could be extracted from the documents")
                    return
                
                text_chunks = get_text_chunks(combined_text)
                
                if not text_chunks:
                    st.error("No valid text chunks could be created")
                    return
                
                st.info(f"Created {len(text_chunks)} text chunks")
                
                vectorstore = get_vectorstore(text_chunks)
                if vectorstore:
                    st.session_state.conversation = get_conversational_chain(vectorstore)
                    if st.session_state.conversation:
                        st.success("Ready to answer questions!")
                    else:
                        st.error("Failed to initialize conversation chain")

if __name__ == "__main__":
    main()