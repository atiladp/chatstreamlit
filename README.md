# 🤖 ChatPDF - Interaja com seus PDFs usando IA

Este é um projeto desenvolvido com [Streamlit](https://streamlit.io/) e [LangChain](https://www.langchain.com/) que permite ao usuário fazer upload de arquivos PDF e conversar com o conteúdo utilizando um modelo LLM hospedado pela [Groq](https://groq.com/).

---

## 📸 Visão Geral

O usuário pode:

- Fazer upload de arquivos PDF
- Inicializar um chatbot com base no conteúdo dos PDFs enviados
- Fazer perguntas em linguagem natural e obter respostas contextualizadas
- Ver o histórico da conversa
- Receber todas as respostas **em português do Brasil**

---

## 🚀 Como executar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/chatpdf-streamlit.git
cd chatpdf-streamlit
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Crie o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
GROQ_API_KEY=sua_chave_groq_aqui
GROQ_MODEL=llama3-70b-8192
TEMPERATURE=0.1
MAX_TOKENS=4000
VERBOSE=True
```

> 🔐 **Importante**: Não compartilhe seu `.env` publicamente!

---

## ▶️ Como rodar

Execute o Streamlit:

```bash
streamlit run app.py
```

A aplicação abrirá em seu navegador padrão.

---

## 🗂 Estrutura do projeto

```
chatstreamlit/
│
├── app.py                 # Interface Streamlit principal
├── utils.py               # Lógica de carregamento, chunking, embeddings e criação do chatbot
├── requirements.txt       # Dependências do projeto
├── .env                   # Variáveis de ambiente (não deve ser versionado)
├── .gitignore             # Arquivos e pastas ignoradas pelo Git
├── anotacoes.txt          # Arquivo opcional para anotações pessoais
└── files/                 # Pasta onde os PDFs são salvos localmente
```

---

## 🧠 Tecnologias utilizadas

- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [Groq API](https://console.groq.com/)
- [HuggingFace Sentence Transformers](https://www.sbert.net/)
- [FAISS](https://faiss.ai/)
- [Python-dotenv](https://pypi.org/project/python-dotenv/)
- [PyPDF](https://pypi.org/project/pypdf/)

---

## 📌 Observações

- O chatbot está configurado para responder **sempre em português do Brasil**.
- É possível customizar o modelo Groq no arquivo `.env`.
- Todos os arquivos PDF são temporariamente armazenados na pasta `files/`.

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

## 🙋‍♂️ Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma *issue* ou enviar um *pull request*.
