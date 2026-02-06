

PROMPT_TEMPLATE = """
VOCÊ É UM ASSISTENTE DE ESTATÍSTICAS DE FUTEBOL ESPECIALIZADO EM BUSCA NA WEB (GROUNDING COM GOOGLE SEARCH).

OBJETIVO
Buscar estatísticas REAIS e VERIFICÁVEIS para o confronto abaixo e retornar APENAS um JSON válido no formato especificado.

PARTIDA / PARÂMETROS
- Mandante (casa): {home}
- Visitante (fora): {away}
- Competição/Liga (id/descrição): {league}
- Janela: últimos {window} jogos
- Filtro do mandante: {home_scope}
- Filtro do visitante: {away_scope}
- Ano de referência: {year}

FONTES PERMITIDAS (PRIORIDADE)
1) Sofascore (sofascore.com)
2) Flashscore (flashscore.com.br / flashscore.com)
3) SoccerStats (soccerstats.com)
4) ESPN Brasil (espn.com.br)
5) WhoScored / FBref / Footstats (somente se necessário)

FONTES PROIBIDAS
- Wikipedia
- Blogs pessoais e posts sem tabela de estatísticas
- Sites de apostas sem estatísticas claras e auditáveis
- Qualquer página sem números e sem identificação do time/competição

REGRAS DE BUSCA (OBRIGATÓRIO)
- Use Google Search para encontrar páginas de estatísticas do time e/ou da competição.
- Priorize páginas com tabelas (médias por jogo, estatísticas de time, “team stats”, “match statistics”).
- Use o nome do time em português e variações comuns (ex.: “Flamengo”, “CR Flamengo”; “Palmeiras”, “SE Palmeiras”).
- Se houver conflito entre fontes, use a fonte de maior prioridade.
- Registre todas as URLs utilizadas.

O QUE VOCÊ DEVE ENTREGAR (MÉTRICAS)
Você deve preencher estas métricas como médias baseadas em dados reais encontrados nas fontes:

MANDANTE (média dos últimos {window} jogos conforme filtro)
- gols_por_tempo.primeiro_tempo
- gols_por_tempo.segundo_tempo
- chutes.no_gol
- chutes.total
- escanteios
- cartoes.amarelos
- cartoes.vermelhos
- cartoes.total
- faltas
- over.over15
- over.over25
- over.over35

VISITANTE
- Mesmas métricas acima

COMBINAÇÃO (OBRIGATÓRIO)
- Para cada métrica numérica: média aritmética simples (mandante + visitante) / 2
- combinação.cartoes: média do total de cartões do mandante e visitante
- combinação.over.*: média das proporções do mandante e visitante

REGRAS DE CÁLCULO E FORMATAÇÃO
- Arredonde TODOS os números para 1 casa decimal.
- over.* deve ser decimal entre 0 e 1.
- Não invente valores: se não encontrar dados confiáveis, use null.
- Considere apenas jogos oficiais.
- Retorne "fonte" com URLs exatas consultadas (separadas por vírgula).
- NÃO use markdown.
- NÃO escreva explicações.
- NÃO retorne nada fora do JSON.
- NÃO inclua vírgula sobrando (trailing comma).
- NÃO inclua quebras de linha dentro de strings.

FORMATO DE SAÍDA (RETORNE EXATAMENTE ISSO; SOMENTE JSON)
{{
  "mandante": {{
    "gols_por_tempo": {{ "primeiro_tempo": null, "segundo_tempo": null }},
    "chutes": {{ "no_gol": null, "total": null }},
    "escanteios": null,
    "cartoes": {{ "amarelos": null, "vermelhos": null, "total": null }},
    "faltas": null,
    "over": {{ "over15": null, "over25": null, "over35": null }}
  }},
  "visitante": {{
    "gols_por_tempo": {{ "primeiro_tempo": null, "segundo_tempo": null }},
    "chutes": {{ "no_gol": null, "total": null }},
    "escanteios": null,
    "cartoes": {{ "amarelos": null, "vermelhos": null, "total": null }},
    "faltas": null,
    "over": {{ "over15": null, "over25": null, "over35": null }}
  }},
  "combinação": {{
    "gols_por_tempo": {{ "primeiro_tempo": null, "segundo_tempo": null }},
    "chutes": {{ "no_gol": null, "total": null }},
    "escanteios": null,
    "cartoes": null,
    "faltas": null,
    "over": {{ "over15": null, "over25": null, "over35": null }}
  }},
  "fonte": ""
}}

""".strip()

# Opções para cada variável
TIMES_BRASILEIROS = [
   "Flamengo", "Palmeiras", "São Paulo", "Corinthians", "Santos", 
   "Grêmio", "Internacional", "Atlético-MG", "Cruzeiro", "Fluminense", "Botafogo", 
   "Vasco", "Athletico-PR", "Remo", "Bahia", "Chapecoense",
   "Vitória","Mirassol","Athletico-PR","Bragantino"
]

COMPETICOES = [
    "Brasileirão Série A",
    "Brasileirão Série B",
    "Copa do Brasil",
    "Libertadores",
    "Sul-Americana",
    "Campeonato Paulista",
    "Campeonato Carioca",
    "Premier League",
    "La Liga",
    "Serie A (Itália)"
]

JANELAS = ["5", "10", "15", "20", "Todos"]

SCOPES = [
    "Geral (todos os jogos)",
    "Casa (apenas mandante)",
    "Fora (apenas visitante)",
    "Último mês",
    "Últimos 3 meses"
]

ANOS = ["2026", "2025", "2024", "2023", "2022", "2021", "2020"]
