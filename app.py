# Importa a biblioteca Streamlit, usada para criar a interface web.
import random
import streamlit as st
import streamlit.components.v1 as components
# Importa a biblioteca do Google Generative AI para interagir com o modelo Gemini.
import google.generativeai as genai
# Importa a biblioteca os para interagir com o sistema operacional (usada aqui para ler variáveis de ambiente).
import os
# Importa a função load_dotenv da biblioteca python-dotenv para carregar variáveis de ambiente de um arquivo .env.
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env.
load_dotenv()

# --- Configuração do Modelo Gemini ---

# Configura a API do Gemini com a chave que está na variável de ambiente.
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define a instrução de sistema que guiará o comportamento do nosso agente de IA.
# Esta é a parte mais CRÍTICA para o nosso projeto.
# Ela define a "personalidade" e as regras que o nosso tutor deve seguir.
system_instruction = """
Você é um tutor de IA especializado em ajudar estudantes do ensino fundamental e médio. Seu nome é <nome da ia kk>.
Seu objetivo NÃO é dar as respostas prontas. Seu objetivo é guiar o aluno a encontrar a resposta por conta própria.

Siga estritamente as seguintes regras:
1.  **Apresente-se e Peça um Tópico**: Comece a conversa se apresentando como "<nomeIA>" e pergunte ao aluno qual matéria ou tópico ele gostaria de estudar hoje.
2.  **Crie uma Pergunta**: Assim que o aluno disser o tópico, crie uma pergunta ou um problema desafiador, mas apropriado para o nível escolar, sobre esse tópico.
3.  **NUNCA Dê a Resposta Direta**: Em hipótese alguma, forneça a resposta final para a pergunta que você criou.
4.  **Guie com Pistas e Explicações**: Se o aluno não souber a resposta ou errar, quebre o problema em partes menores. Explique os conceitos fundamentais passo a passo. Use analogias simples e exemplos do dia a dia.
5.  **Verifique a Compreensão**: A cada pequena explicação, faça uma pergunta para verificar se o aluno está entendendo. Use frases como "Fez sentido pra você?", "Consegue pensar em um exemplo disso?", "O que você acha que vem a seguir?".
6.  **Seja Encorajador e Paciente**: Mantenha um tom positivo e motivador. Elogie o esforço do aluno. Frases como "Ótima tentativa!", "Estamos quase lá!", "Excelente pergunta!" são muito bem-vindas.
7.  **Conduza à Resposta**: Continue dando pistas e explicando os conceitos até que o próprio aluno consiga formular a resposta correta. Quando ele acertar, parabenize-o e faça um breve resumo do que foi aprendido.
8.  **Explique a lógica, analogias, etc., de forma que crianças e adolescente entendam de maneira fácil.
"""

# Inicializa o modelo generativo do Gemini, especificando o modelo a ser usado ('gemini-1.5-pro-latest').
# Passa a instrução de sistema para definir o comportamento do modelo.
# MUDAR VERSÃO
model = genai.GenerativeModel(
    model_name="gemini-2.5-fast",
    system_instruction=system_instruction
)

# --- Interface do Streamlit ---

# Define o título da página da aplicação web.
st.title("🤖 AprendaAI: Seu Tutor de IA")
# Escreve um subtítulo ou uma descrição breve para o usuário.
st.write("Olá! Eu sou o <nomeIA>. Estou aqui para te ajudar a aprender, não para te dar as respostas. Vamos estudar juntos?")

# Verifica se o 'chat' (a sessão de conversa) já foi inicializado no estado da sessão do Streamlit.
if "chat" not in st.session_state:
    # Se não foi, inicia uma nova sessão de chat com o modelo Gemini.
    st.session_state.chat = model.start_chat(history=[])

# Itera sobre o histórico de mensagens armazenado no estado da sessão.
# O histórico é uma lista de dicionários, onde cada dicionário representa uma mensagem.
for message in st.session_state.chat.history:
    # Define o "avatar" a ser exibido ao lado da mensagem, dependendo do papel ('user' ou 'model').
    avatar = "👤" if message.role == "user" else "🤖"
    # Usa st.chat_message para exibir a mensagem na interface de chat com o avatar apropriado.
    with st.chat_message(message.role, avatar=avatar):
        # Exibe o conteúdo da mensagem (a parte de texto).
        st.markdown(message.parts[0].text)

#lista de frases para o placeholder
listTextsPlaceholderInputPrompt = ["O que deseja saber? (:", "Qual matéria você prefere revisar hoje?",
             "O que você gostaria de estudar agora?", "Qual disciplina está com mais vontade de focar hoje?",
             "Que assunto você quer aprender neste momento?", "Qual matéria você acha melhor começar hoje?",
             "O que você gostaria de revisar primeiro?", "Qual disciplina você está a fim de estudar hoje?",
            "Que tema você prefere aprofundar agora?", "Qual matéria você sente que precisa praticar hoje?",
            "O que você quer estudar nesta sessão?"
             ]
#gerando índice aleatório de 1 a 11
indexTexts = random.randint(0, 10) 

# Cria um campo de entrada de texto na parte inferior da tela, com um placeholder.
# A variável 'prompt' conterá o texto que o usuário digitar.
# com placeholder randomizado
if prompt := st.chat_input(listTextsPlaceholderInputPrompt[indexTexts]):
    # Exibe a mensagem do usuário na interface de chat imediatamente.
    with st.chat_message("user", avatar="👤"):
        # Mostra o prompt que o usuário digitou.
        st.markdown(prompt)

    # Envia a mensagem do usuário para o modelo Gemini e aguarda a resposta.
    # O Streamlit mostrará um indicador de "rodando" enquanto espera.
    response = st.session_state.chat.send_message(prompt)

    # Exibe a resposta do modelo (do nosso tutor IA) na interface de chat.
    with st.chat_message("model", avatar="🤖"):
        # Mostra o texto da resposta recebida do Gemini.
        st.markdown(response.text)

#codigo html
components.html(
    """
        
    """,
    height=300
)

#código css
st.markdown(
    """
        <style>
            *{
                
            }
        </style>

    """,
    unsafe_allow_html=True
)