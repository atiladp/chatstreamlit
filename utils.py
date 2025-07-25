# Importa bibliotecas padrão e específicas do LangChain, Streamlit e outros utilitários
import os
from pathlib import Path
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_community.vectorstores.faiss import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings

# Carrega variáveis de ambiente do arquivo .env
_ = load_dotenv(find_dotenv())

# Define o caminho da pasta onde os arquivos PDF estão localizados
folder_files = Path(__file__).parent / "files"

# Função para carregar os documentos PDF da pasta especificada
def importacao_documentos():
    """Importa todos os documentos PDF da pasta files"""
    documentos = []
    for arquivo in folder_files.glob("*.pdf"):
        loader = PyPDFLoader(str(arquivo))  # Usa PyPDFLoader para ler o conteúdo
        documentos_arquivo = loader.load()  # Carrega o conteúdo do PDF
        documentos.extend(documentos_arquivo)  # Adiciona ao conjunto de documentos
    return documentos

# Fucnção para dividir os documentos em partes menores (hunks)
def split_documentos(documentos):
    """Divide os documentos em chunks menores"""
    recur_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,              # Tamanho de cada chunk
        chunk_overlap=50,             # Sobreposição entre chunks
        separators=["\n\n", "\n", ".", " ", ""]  # Separadores usados na divisão
    )
    documentos = recur_splitter.split_documents(documentos)
    
    # Adiciona metadados para rastrear a origem e o ID de cada chunk
    for i, doc in enumerate(documentos):
        doc.metadata["source"] = doc.metadata["source"].split("/")[-1]
        doc.metadata["doc_id"] = i
    return documentos

# Função para criar um vector store FAISS com embeddings do HuggingFace
def cria_vector_store(documentos):
    """Cria o vector store usando FAISS e HuggingFace embeddings (gratuito)"""
    try:
        # Usando embeddings gratuitos do HuggingFace
        embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",  # Modelo leve e eficiente
            model_kwargs={'device': 'cpu'},                        # Usa CPU
            encode_kwargs={'normalize_embeddings': True}          # Normaliza embeddings
        )
        
        # Cria o vector store FAISS a partir dos documentos
        vector_store = FAISS.from_documents(
            documents=documentos,
            embedding=embedding_model
        )
        return vector_store
    except Exception as e:
        # Exibe erro no Streamlit se falhar
        st.error(f"Erro ao criar vector store: {str(e)}")
        return None

# Função principal para criar a cadeia de conversação
def cria_chain_conversa():
    """Cria a chain de conversação usando apenas Groq"""
    try:
        # Verifica se a chave da API do Groq está configurada no .env
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            st.error("Chave da API Groq não encontrada. Verifique o arquivo .env")
            return None
        
        # Carrega configurações opcionais do .env
        model_name = os.getenv("GROQ_MODEL", "llama3-70b-8192")
        temperature = float(os.getenv("TEMPERATURE", "0.1"))
        max_tokens = int(os.getenv("MAX_TOKENS", "4000"))
        verbose = os.getenv("VERBOSE", "True").lower() == "true"
        
        # Carrega e prepara os documentos
        documentos = importacao_documentos()
        if not documentos:
            st.error("Nenhum documento PDF encontrado na pasta files")
            return None
            
        documentos = split_documentos(documentos)
        vector_store = cria_vector_store(documentos)
        
        if not vector_store:
            return None
        
        # Inicializa o modelo de linguagem da Groq com as configurações fornecidas
        chat = ChatGroq(
            api_key=groq_api_key,
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            verbose=verbose
        )
        
        # Cria a memória para armazenar o histórico de conversa
        memory = ConversationBufferMemory(
            return_messages=True,             # Retorna mensagens completas
            memory_key="chat_history",        # Chave usada na chain
            output_key="answer"               # Onde será armazenada a resposta
        )
        
        # Define o mecanismo de busca baseado em similaridade (top 3 mais relevantes)
        retriever = vector_store.as_retriever(
            search_kwargs={"k": 3}
        )
        
        # Cria a cadeia de conversa com recuperação de documentos
        chat_chain = ConversationalRetrievalChain.from_llm(
            llm=chat,
            memory=memory,
            retriever=retriever,
            return_source_documents=True,     # Retorna também as fontes dos documentos
            verbose=verbose
        )
        
        # Armazena a chain no estado da sessão do Streamlit
        st.session_state["chain"] = chat_chain
        return chat_chain
        
    except Exception as e:
        # Exibe erro no Streamlit se algo der errado
        st.error(f"Erro ao criar chain de conversação: {str(e)}")
        return None
