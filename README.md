Assistente de Investimentos com Interface Gráfica e IA
Descrição
Este projeto é um assistente de investimentos pessoal desenvolvido em Python, com uma interface gráfica criada com a biblioteca CustomTkinter. A aplicação permite ao usuário gerenciar sua carteira de ativos financeiros de forma local, além de oferecer análises sobre o mercado financeiro utilizando a IA Generativa do Google Gemini.

adicione aqui um screenshot da sua aplicação em funcionamento.

Funcionalidades
Interface Gráfica: Gerencie sua carteira através de uma interface de usuário clara e funcional.

Gerenciamento de Carteira:

Adicione novos ativos ou atualize a quantidade e o preço médio dos existentes.

Remova ativos da sua carteira.

Visualize um resumo do seu portfólio, com valor total investido por ativo e patrimônio total.

Persistência de Dados: A carteira do usuário é salva automaticamente em um arquivo carteira.json.

Análise de Notícias com IA: O assistente busca notícias recentes do mercado financeiro (via feed RSS do InfoMoney) e utiliza a API do Google Gemini para fornecer uma análise sobre como os eventos atuais podem impactar os ativos da carteira do usuário.

Tecnologias Utilizadas
Tecnologia	Finalidade
Python	Linguagem principal do projeto.
CustomTkinter	Biblioteca para a criação da interface gráfica.
Google Gemini	Modelo de IA para a análise de notícias.
Feedparser	Biblioteca para ler e extrair notícias de feeds RSS.
Dotenv	Gerenciamento da chave de API em variáveis de ambiente.
Como Executar
Siga os passos abaixo para configurar e rodar o projeto em sua máquina local.

Pré-requisitos
Python 3.8 ou superior instalado.

Git instalado para clonar o repositório.

Uma chave de API do Google Gemini, que pode ser obtida no Google AI Studio.

Passo a Passo
Clone o repositório:

Bash

git clone https://github.com/caualeal-dev/assistente-financeiro-ia.git
cd assistente-financeiro-ia
(Nota: Crie um repositório com o nome assistente-financeiro-ia em seu perfil para que este link funcione)

Crie e ative um ambiente virtual:

Bash

# Para Windows
python -m venv venv
.\venv\Scripts\activate

# Para macOS/Linux
python3 -m venv venv
source venv/bin/activate
Crie o arquivo de dependências requirements.txt com o seguinte conteúdo:

Plaintext

customtkinter
google-generativeai
feedparser
python-dotenv
Instale as dependências:

Bash

pip install -r requirements.txt
Configure sua chave de API:

Crie um arquivo chamado .env na raiz do projeto.

Dentro dele, adicione sua chave da API do Gemini da seguinte forma:

GEMINI_API_KEY="SUA_CHAVE_DE_API_REAL_VAI_AQUI"
Executando a Aplicação
Com a configuração concluída, execute o arquivo da interface gráfica para iniciar o assistente:

Bash

python gui_agente.py
