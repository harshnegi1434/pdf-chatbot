import os
import dill
import streamlit as st
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Function to read PDF content
def read_pdf(file_path):
    pdf_reader = PdfReader(file_path)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


# Mapping of PDFs
pdf_mapping = {
    'American Economy': 'AmericanEconomyWithCovers.pdf',
    'Indian Economy' : 'TheIndianEconomy.pdf'    
}

# Load environment variables
load_dotenv()

# Main Streamlit app
def main():
    st.title("PDF CHATBOT")
    with st.sidebar:
        st.title('Ask Questions From PDF')
        st.markdown('''
        ## About
        Choose the desired PDF, then perform a query.
        ''')

    custom_names = list(pdf_mapping.keys())
    custom_names.append("Upload PDF")
    selected_custom_name = st.sidebar.selectbox('Choose your PDF', custom_names)
    
    if selected_custom_name == "Upload PDF":
        uploaded_file = st.sidebar.file_uploader("Upload PDF", type=["pdf"])
        if uploaded_file:
            file_path = f"temp_{uploaded_file.name}"
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
        else:
            file_path = None
    else:
        selected_actual_name = pdf_mapping.get(selected_custom_name)
        pdf_folder = "pdfs"
        file_path = os.path.join(pdf_folder, selected_actual_name)

    if file_path:
        try:
            text = read_pdf(file_path)
            st.info("The content of the PDF is hidden. Type your query in the chat window.")
        except FileNotFoundError:
            st.error(f"File not found: {file_path}")
            return
        except Exception as e:
            st.error(f"Error occurred while reading the PDF: {e}")
            return

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
            length_function=len
        )

        # Process the PDF text and create the documents list
        documents = text_splitter.split_text(text=text)

        # Vectorize the documents and create vectorstore
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_texts(documents, embedding=embeddings)

        st.session_state.processed_data = {
            "document_chunks": documents,
            "vectorstore": vectorstore,
        }

        # Save vectorstore using pickle
        pickle_folder = "Pickle"
        if not os.path.exists(pickle_folder):
            os.mkdir(pickle_folder)

        pickle_file_path = os.path.join(pickle_folder, f"{selected_custom_name}.pkl")

        if not os.path.exists(pickle_file_path):
            with open(pickle_file_path, "wb") as f:
                dill.dump(vectorstore, f)

        # Load the Langchain chatbot
        llm = ChatOpenAI(temperature=0, max_tokens=1000, model_name="gpt-3.5-turbo")
        qa = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever())

        # Initialize Streamlit chat UI
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input(f"Ask your questions from PDF '{selected_custom_name}'"):
            st.session_state.messages = []  # Reset the chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            result = qa({"question": prompt, "chat_history": [(message["role"], message["content"]) for message in st.session_state.messages]})
            print(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = result["answer"]
                message_placeholder.markdown(full_response + "|")
            message_placeholder.markdown(full_response)
            print(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()
