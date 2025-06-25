# main_app.py
import streamlit as st
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQAWithSourcesChain
import app_setup
from authenticator import get_authenticator,login_fields # Import authenticator setup

# ------------------ AUTHENTICATION ------------------
authenticator = get_authenticator()
name, authentication_status, username = authenticator.login(fields=login_fields)

# ------------------ MAIN APP ------------------
if authentication_status:
    st.sidebar.title(f"Welcome {name} 👋")
    st.sidebar.write("Select an option below:")
    st.sidebar.button("Home")
    st.sidebar.button("Settings")

    # Session state init
    if 'URL_INPUT' not in st.session_state:
        st.session_state.URLS_INPUT = []
    if 'check' not in st.session_state:
        st.session_state.check = False
    if 'vectorindex_gemini' not in st.session_state:
        st.session_state.vectorindex_gemini = None

    # Sidebar URL inputs
    st.sidebar.header('Enter the URLs')
    url_1 = st.sidebar.text_input('URL 1')
    url_2 = st.sidebar.text_input('URL 2')
    url_3 = st.sidebar.text_input('URL 3')
    process = st.sidebar.button('Process URLs')

    st.header('GEN AI: News Research Tool')
    question = st.text_input("Enter your question here")

    if process:
        urls = [url_1, url_2, url_3]
        st.write("Processing the following URLs:", urls)

        loader = UnstructuredURLLoader(urls=urls)
        data = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            separators=['\n', '\n\n', '.', ','],
            chunk_size=1000
        )
        docs = text_splitter.split_documents(data)

        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        st.session_state.vector_index_gemini_api = FAISS.from_documents(docs, embeddings)
        st.session_state.vector_index_gemini_api.save_local('faiss_index')
        st.session_state.check = True
        st.success("URLs processed and vector store created!")
        
    response=None
    if st.session_state.check:
        if question:
             vectorindex_gemini = FAISS.load_local(
            'faiss_index',
            GoogleGenerativeAIEmbeddings(model="models/embedding-001"),
            allow_dangerous_deserialization=True
        )
        chain = RetrievalQAWithSourcesChain.from_llm(
            llm=app_setup.llm,
            retriever=vectorindex_gemini.as_retriever()
        )

        response = chain({"question": question})
        st.write("### Answer")
        st.write(response["answer"])
        st.write("### Sources")
        st.write(response.get("sources", "No sources found."))

elif authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")
    
authenticator.logout("Logout","sidebar")