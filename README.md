# Beteste – Estatísticas de Futebol 

Aplicação desktop em Python que utiliza IA para buscar e consolidar estatísticas reais de partidas de futebol em formato JSON.

A interface permite selecionar times, competição, janela de jogos e filtros, enviando a solicitação para um modelo de linguagem via API Groq.

---

## Funcionalidades

* Interface gráfica em Tkinter
* Seleção de times e competição
* Busca de estatísticas com IA
* Retorno em formato JSON estruturado
* Botão para copiar resultado
* Execução em thread para evitar travamentos

---

## Estrutura do projeto

```
beteste/
│
├── main.py          # Ponto de entrada da aplicação
├── gui.py           # Interface gráfica
├── api_client.py    # Comunicação com a API Groq
├── constants.py     # Dados estáticos e template de prompt
├── config.py        # Configurações da API
├── requirements.txt
└── README.md
```

---

## Requisitos

* Python 3.9 ou superior
* Conta na Groq com chave de API

---

## Instalação

1. Clone o repositório:

```
git clone https://github.com/CelsoAntunesNogueira/Betest.git
cd Betest
```

2. Crie um ambiente virtual (recomendado):

### Windows

```
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências:

```
pip install -r requirements.txt
```

---

## Configuração da API

Abra o arquivo `config.py` e insira sua chave da Groq:

```python
GROQ_API_KEY = "sua_chave_aqui"
```

Você pode obter a chave em:
[https://console.groq.com/](https://console.groq.com/)

---

## Executando o projeto

No terminal, dentro da pasta do projeto:

```
python main.py
```

A interface será aberta e você poderá selecionar os times e buscar as estatísticas.

---

## Observações importantes

* A aplicação depende de respostas da IA, que podem variar conforme as fontes disponíveis.
* O JSON retornado é formatado automaticamente, mas pode conter valores `null` caso os dados não sejam encontrados.
* Requer conexão com a internet.

---

## Tecnologias utilizadas

* Python
* Tkinter
* Requests
* Groq API
* Modelo Llama 3.1

---

## Possíveis melhorias futuras

* Armazenamento de histórico de buscas
* Exportação para CSV ou Excel
* Versão web com FastAPI
* Sistema de cache de estatísticas
* Validação automática das respostas da IA

---

## Licença

Projeto de estudo e prototipagem.
