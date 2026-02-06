# ⚽ Soccer Stats AI - Beteste

Assistente inteligente que utiliza IA para buscar, processar e consolidar estatísticas reais de confrontos de futebol diretamente da web.

## 🏗️ Arquitetura do Projeto
O projeto foi refatorado utilizando o princípio de **Separação de Preocupações (SoC)**, dividindo a aplicação em módulos independentes para facilitar a manutenção e escalabilidade:

* **`main.py`**: Ponto de entrada da aplicação.
* **`gui.py`**: Interface gráfica (TKinter) e gerenciamento de estados da UI.
* **`api_client.py`**: Motor de comunicação com a API Groq e tratamento de respostas.
* **`constants.py`**: Centralização de dados estáticos (listas de times, competições e prompts).
* **`config.py`**: Gerenciamento de variáveis de ambiente e chaves de API.

## 🛠️ Tecnologias Utilizadas
* **Python 3.x**
* **IA Generativa**: Groq Cloud (Modelo Llama 3.1 8B).
* **Interface Gráfica**: Tkinter com suporte a ScrollView e Threads.
* **Conectividade**: Requests para consumo de API REST.
* **Processamento de Dados**: JSON para estruturação de métricas.

## 🌟 Funcionalidades
- [x] Busca automática por médias de gols, chutes, escanteios e cartões.
- [x] Filtros específicos por contexto (Geral, Casa ou Fora).
- [x] Execução de requisições em **Threading** (evita o travamento da interface).
- [x] Formatação automática de JSON para integração com outras ferramentas.
