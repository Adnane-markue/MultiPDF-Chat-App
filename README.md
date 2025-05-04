# 📚 Document Chat App

This is a Streamlit-based application that allows you to **chat with multiple documents** (PDF and DOCX). It uses **Google's Gemini Pro (via Langchain)** for question answering, document retrieval, and conversational memory.

Users can upload multiple documents and ask questions about them using a natural language interface.

---

## 🧠 Features

- ✅ Upload multiple PDF and DOCX files
- ✅ Automatically extract and chunk document text
- ✅ Vectorize text using Google Generative AI Embeddings
- ✅ Chat with the content using Gemini 2.0 Flash
- ✅ Retain memory across a conversation
- ✅ User-friendly Streamlit interface
- ✅ Customizable chat interface (HTML templates)

---

## 📸 Demo

### Document Upload

![Upload Screenshot][def]

### Chat Interface

![Chat Screenshot][def2]
![Chat Screenshot][def3]

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Adnane-markue/MultiPDF-Chat-App.git

cd document-chat-app
```
### 2. Create a virtual environment

```bash
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```
### 3. Install dependencies

```bash
pip install -r requirements.txt
```
### 4. Set up environment variables 
Create a **.env** file in the root directory and add your Google Generative AI API key like so:
    
    ```bash
    GOOGLE_API_KEY=your_google_api_key_here
    ```
### 5. Run the app
    
    ```bash
    streamlit run app.py
    ```

## How It Works
1- The app extracts text from uploaded PDFs and DOCX files.

2- Text is split into chunks (chunk size: 1000 characters, 200 overlap).

3- Each chunk is embedded using Google Generative AI Embeddings (embedding-001).

4- Chunks are stored in a FAISS vector store for similarity-based retrieval.

5- A Conversational Retrieval Chain using gemini-2.0-flash is created to answer questions based on retrieved chunks.

6- Conversation history is maintained with a memory buffer to allow follow-up questions.

## UI Overview
- The main screen allows users to ask questions.

- The sidebar allows file uploads and kicks off the document processing.

- Uses custom HTML templates for a more polished chat appearance.

## 📂 File Structure
```plaintext
document-chat-app/  
    ├── app.py                  # Main Streamlit app
    ├── htmlTemplates.py        # HTML/CSS for user/bot message cards
    ├── .env                    # Environment variables (not tracked in git)
    ├── requirements.txt        # Python dependencies
    ├── README.md               # Project readme (this file)
    └── screenshots/            # Optional folder for UI screenshots
```
## 🛠️ Tech Stack

- Streamlit – for the user interface

+ LangChain – for chaining LLMs and retrieval

+ Google Generative AI – for embeddings and Gemini chat model

- FAISS – for efficient vector similarity search

- PyPDF2, python-docx – for document parsing

## ✨ Future Enhancements

- Add support for TXT/CSV file types

- Add option to download chat history

- Support for multilingual document QA

- Add option to download chat history

- Enable persistent vectorstore using a database

## 📬 Contact
If you have questions or ideas for improvement, feel free to open an issue or reach out.






[def]: screenshots/upload.png
[def2]: screenshots/chat_1.png
[def3]: screenshots/chat_2.png