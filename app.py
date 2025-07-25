# Importa as bibliotecas necessárias
import streamlit as st
import time
from pathlib import Path
from utils import cria_chain_conversa

# Define o caminho para a pasta onde os PDFs serão salvos
folder_files = Path(__file__).parent / "files"

# Função principal que lida com a interface do chat
def chat_window():
    # Exibe o cabeçalho do chat
    st.header("🤖 Bem Vindo ao ChatPDF", divider=True)
    
    # Verifica se a cadeia de conversa já foi inicializada
    if not 'chain' in st.session_state:
        st.error("Faça o upload de PDFs para começar")
        st.stop()
    
    # Recupera a cadeia e a memória da conversa
    chain = st.session_state["chain"]
    memory = chain.memory 

    # Recupera o histórico de mensagens da memória
    mensagens = memory.load_memory_variables({})["chat_history"]
    
    # Cria um contêiner para as mensagens do chat
    container = st.container()
    
    # Renderiza todas as mensagens anteriores no chat
    for mensagem in mensagens:
        chat = container.chat_message(mensagem.type)
        chat.markdown(mensagem.content)
        
    # Cria o campo de entrada para nova mensagem do usuário
    nova_mensagem = st.chat_input("Converse com seus documentos")
    
    # Se o usuário enviar uma nova mensagem
    if nova_mensagem:
        # Mostra a mensagem do usuário no chat
        chat = container.chat_message("human")
        chat.markdown(nova_mensagem)
        
        # Cria espaço para a resposta do bot
        chat = container.chat_message("ai")
        placeholder = chat.empty()
        placeholder.markdown("Gerando resposta...")
        
        # Chama a cadeia com a pergunta do usuário
        resposta = chain.invoke({"question": nova_mensagem})
        
        # Substitui o placeholder pela resposta do bot
        placeholder.markdown(resposta["answer"])
        
        # Recarrega a aplicação para atualizar o histórico
        st.rerun()

# Função que salva os arquivos enviados pelo usuário
def save_uploaded_files(uploaded_files, folder):
    """Salva arquivos enviados na pasta especificada."""
    # Cria a pasta se ela ainda não existir
    folder.mkdir(exist_ok=True)
    
    # Remove arquivos antigos na pasta
    for file in folder.glob("*.pdf"):
        file.unlink()
    
    # Salva os novos arquivos PDF enviados
    for file in uploaded_files:
        (folder / file.name).write_bytes(file.read())

# Função principal da aplicaçãos
def main():
    # Define o conteúdo da barra lateral
    with st.sidebar:
        st.header("Upload de PDFs")
        
        # Permite o upload de múltiplos arquivos PDF
        uploaded_pdfs = st.file_uploader("Adicione arquivos PDF", 
                                         type="pdf", 
                                         accept_multiple_files=True)
        
        # Se arquivos foram enviados, salva-os
        if uploaded_pdfs:
            save_uploaded_files(uploaded_pdfs, folder_files)
            st.success(f"{len(uploaded_pdfs)} arquivo(s) salvo(s) com sucesso!")
        
        # Define o rótulo do botão conforme o estado atual
        label_botao = "Inicializar Chatbot"
        if "chain" in st.session_state:
            label_botao = "Atualizar Chatbot"
        
        # Botão para inicializar ou atualizar o chatbot
        if st.button(label_botao, use_container_width=True):
            # Verifica se existem arquivos PDF para iniciar o bot
            if len(list(folder_files.glob("*.pdf"))) == 0:
                st.error("Adicione arquivos pdf para inicializar o chatbot")
            else:
                with st.spinner("Inicializando o Chatbot..."):
                    try:
                        # Cria a cadeia de conversa
                        cria_chain_conversa()
                        st.success("Chatbot inicializado com sucesso!")
                        st.rerun()
                    except Exception as e:
                        # Exibe erro caso a inicialização falhe
                        st.error(f"Erro ao inicializar o chatbot: {str(e)}")
    
    # Exibe a janela de chat
    chat_window()

# Ponto de entrada do script
if __name__ == "__main__":
    main()
