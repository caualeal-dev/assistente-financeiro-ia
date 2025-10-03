import os
import json
import feedparser
import google.generativeai as genai
from dotenv import load_dotenv

NOME_ARQUIVO_CARTEIRA = "carteira.json"
load_dotenv()

# --- Funções de Gerenciamento da Carteira ---

def carregar_carteira():
    """Carrega a carteira de investimentos do arquivo JSON."""
    try:
        with open(NOME_ARQUIVO_CARTEIRA, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def salvar_carteira(carteira):
    """Salva a carteira de investimentos no arquivo JSON."""
    with open(NOME_ARQUIVO_CARTEIRA, 'w', encoding='utf-8') as f:
        json.dump(carteira, f, indent=4, ensure_ascii=False)

# --- Faz a formatação para texto ---
def formatar_carteira_para_texto(carteira):
    """Formata o dicionário da carteira em um texto legível para exibição."""
    if not carteira:
        return "Sua carteira está vazia."
    
    texto_formatado = "--- Sua Carteira de Investimentos ---\n\n"
    patrimonio_total = 0
    for ticker, dados in carteira.items():
        # Usamos .get() para evitar erros se a chave não existir
        quantidade = dados.get('quantidade', 0)
        preco_medio = dados.get('preco_medio', 0)
        valor_total_ativo = quantidade * preco_medio
        patrimonio_total += valor_total_ativo
        texto_formatado += f"Ativo: {ticker.upper()}\n"
        texto_formatado += f"  Quantidade: {quantidade}\n"
        texto_formatado += f"  Preço Médio: R$ {preco_medio:.2f}\n"
        texto_formatado += f"  Valor Investido: R$ {valor_total_ativo:.2f}\n"
        texto_formatado += "-" * 25 + "\n"
    texto_formatado += f"\nPATRIMÔNIO TOTAL INVESTIDO: R$ {patrimonio_total:.2f}\n"
    return texto_formatado

# --- Funções de Análise com IA ---

def configurar_ia():
    """Configura e retorna o modelo de IA do Gemini."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Chave de API do Gemini não encontrada.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def analisar_noticias_relevantes(carteira, modelo_ia):
    """Busca notícias e usa a IA para analisar o impacto nos ativos da carteira."""
    if not carteira:
        return "Sua carteira está vazia. Adicione ativos para receber análises."

    tickers = list(carteira.keys())
    # Corrigindo o pequeno erro de digitação na URL
    url_feed = 'https://www.infomoney.com.br/feed/'
    feed = feedparser.parse(url_feed)
    titulos_noticias = [entry.title for entry in feed.entries[:10]]
    
    prompt = f"""
    Você é um assistente de educação financeira direto.
    Analise a lista de títulos de notícias e identifique se alguma impacta os ativos da minha carteira.

    Minha Carteira: {', '.join(tickers)}
    Títulos: {'; '.join(titulos_noticias)}

    Para cada notícia relevante, formate a resposta como:
    - Título: [Título da notícia]
    - Análise: [Explicação do impacto].
    """
    
    try:
        response = modelo_ia.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erro ao gerar análise da IA: {e}"