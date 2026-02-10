from config import GROQ_API_KEY, GROQ_API_URL, GROQ_MODEL
import tkinter as tk
from tkinter import Tk,scrolledtext, messagebox,ttk, Frame, Label
from constants import TIMES_BRASILEIROS, COMPETICOES, JANELAS, SCOPES, ANOS, PROMPT_TEMPLATE
from api_client import enviar_para_groq, formatar_json
import requests
import threading
import json
 
class EstatisticasFutebolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Beteste")
        self.root.geometry("1030x780")
        self.root.resizable(True, True)
        
        # Configurar cores
        self.bg_color = "#233024"
        self.fg_color = "#cdd6f4"
        self.accent_color = "#ffffff"
        self.button_color = "#24940e"
        self.card_bg = "#313244"
        self.root.configure(bg=self.bg_color)
        
        self.criar_interface()
    
    def criar_interface(self):
        # Status bar (PRIMEIRO - antes do canvas e scrollbar)
        self.status_label = tk.Label(
            self.root,
            text="Pronto para buscar estatísticas! ",
            font=("Arial", 9),
            bg="#233024",
            fg=self.fg_color,
            anchor="w",
            padx=10
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Container principal com scroll
        canvas = tk.Canvas(self.root, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Adicionar scroll com a roda do mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Título
        titulo = tk.Label(
            scrollable_frame,
            text=" Estatísticas de Futebol",
            font=("Arial", 22, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        titulo.pack(pady=15)
        
        # Subtítulo
        subtitulo = tk.Label(
            scrollable_frame,
            text="Busca inteligente de estatísticas verificáveis de partidas",
            font=("Arial", 10),
            bg=self.bg_color,
            fg=self.fg_color
        )
        subtitulo.pack(pady=(0, 15))
        
        # Frame principal com duas colunas
        main_container = tk.Frame(scrollable_frame, bg=self.bg_color)
        main_container.pack(padx=20, fill="both", expand=True)
        
        # COLUNA ESQUERDA - Formulários
        left_frame = tk.Frame(main_container, bg=self.bg_color)
        left_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=(0, 10))
        
        # COLUNA DIREITA - Resultado
        right_frame = tk.Frame(main_container, bg=self.bg_color)
        right_frame.pack(side=tk.RIGHT, fill="both", expand=True, padx=(10, 0))
        
        # ========== COLUNA ESQUERDA ==========
        
        # ===== TIMES =====
        times_frame = tk.LabelFrame(
            left_frame,
            text="   Times  ",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            fg=self.accent_color,
            labelanchor="n"
        )
        times_frame.pack(fill="x", pady=10)
        
        # Container interno para usar grid
        times_inner = tk.Frame(times_frame, bg=self.bg_color)
        times_inner.pack(padx=10, pady=10, fill="x")
        
        # Mandante
        tk.Label(times_inner, text="Mandante (Casa):", font=("Arial", 10), 
                bg=self.bg_color, fg=self.fg_color, width=20, anchor="w").grid(row=0, column=0, sticky="w", pady=5)
        self.combo_home = ttk.Combobox(times_inner, values=TIMES_BRASILEIROS, 
                                       state="readonly", font=("Arial", 10))
        self.combo_home.set("Selecione o time da casa...")
        self.combo_home.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=5)
        
        # Visitante
        tk.Label(times_inner, text="Visitante (Fora):", font=("Arial", 10), 
                bg=self.bg_color, fg=self.fg_color, width=20, anchor="w").grid(row=1, column=0, sticky="w", pady=5)
        self.combo_away = ttk.Combobox(times_inner, values=TIMES_BRASILEIROS, 
                                       state="readonly", font=("Arial", 10))
        self.combo_away.set("Selecione o time visitante...")
        self.combo_away.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=5)
        
        # Configurar para que a coluna dos comboboxes expanda
        times_inner.columnconfigure(1, weight=1)
        
        # ===== COMPETIÇÃO E CONTEXTO =====
        contexto_frame = tk.LabelFrame(
            left_frame,
            text="   Competição e Contexto  ",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            fg=self.accent_color,
            labelanchor="n"
        )
        contexto_frame.pack(fill="x", pady=10)
        
        # Container interno
        contexto_inner = tk.Frame(contexto_frame, bg=self.bg_color)
        contexto_inner.pack(padx=10, pady=10, fill="x")
        
        # Competição
        tk.Label(contexto_inner, text="Competição:", font=("Arial", 10), 
                bg=self.bg_color, fg=self.fg_color).pack(anchor="w", pady=(0, 2))
        self.combo_league = ttk.Combobox(contexto_inner, values=COMPETICOES, 
                                         state="readonly", font=("Arial", 10))
        self.combo_league.set("Brasileirão Série A")
        self.combo_league.pack(fill="x", pady=(0, 10))
        
        # Janela
        tk.Label(contexto_inner, text="Janela (jogos):", font=("Arial", 10), 
                bg=self.bg_color, fg=self.fg_color).pack(anchor="w", pady=(0, 2))
        self.combo_window = ttk.Combobox(contexto_inner, values=JANELAS, 
                                         state="readonly", font=("Arial", 10))
        self.combo_window.set("10")
        self.combo_window.pack(fill="x", pady=(0, 10))
        
        # Ano
        tk.Label(contexto_inner, text="Ano:", font=("Arial", 10), 
                bg=self.bg_color, fg=self.fg_color).pack(anchor="w", pady=(0, 2))
        self.combo_year = ttk.Combobox(contexto_inner, values=ANOS, 
                                       state="readonly", font=("Arial", 10))
        self.combo_year.set("2026")
        self.combo_year.pack(fill="x", pady=(0, 10))
        
        # ===== FILTROS =====
        filtros_frame = tk.LabelFrame(
            left_frame,
            text=" Filtros de Análise  ",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            fg=self.accent_color,
            labelanchor="n"
        )
        filtros_frame.pack(fill="x", pady=10)
        
        # Container interno para usar grid
        filtros_inner = tk.Frame(filtros_frame, bg=self.bg_color)
        filtros_inner.pack(padx=10, pady=10, fill="x")
        
        # Filtro Mandante
        tk.Label(filtros_inner, text="Filtro do Mandante:", font=("Arial", 10), 
                bg=self.bg_color, fg=self.fg_color, width=20, anchor="w").grid(row=0, column=0, sticky="w", pady=5)
        self.combo_home_scope = ttk.Combobox(filtros_inner, values=SCOPES, 
                                             state="readonly", font=("Arial", 10))
        self.combo_home_scope.set("Geral (todos os jogos)")
        self.combo_home_scope.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=5)
        
        # Filtro Visitante
        tk.Label(filtros_inner, text="Filtro do Visitante:", font=("Arial", 10), 
                bg=self.bg_color, fg=self.fg_color, width=20, anchor="w").grid(row=1, column=0, sticky="w", pady=5)
        self.combo_away_scope = ttk.Combobox(filtros_inner, values=SCOPES, 
                                             state="readonly", font=("Arial", 10))
        self.combo_away_scope.set("Geral (todos os jogos)")
        self.combo_away_scope.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=5)
        
        # Configurar para que a coluna dos comboboxes expanda
        filtros_inner.columnconfigure(1, weight=1)
        
        # ===== BOTÃO GERAR =====
        self.btn_gerar = tk.Button(
            left_frame,
            text=" Buscar Estatísticas",
            font=("Arial", 13, "bold"),
            bg=self.button_color,
            fg="#ffffff",
            activebackground="#44a83b",
            cursor="hand2",
            padx=30,
            pady=12,
            border=0,
            command=self.buscar_estatisticas
        )
        self.btn_gerar.pack(pady=15)
        
        # Frame para botões inferiores
        btn_frame = tk.Frame(left_frame, bg=self.bg_color)
        btn_frame.pack(pady=10)
        
        # Botão Limpar
        btn_limpar = tk.Button(
            btn_frame,
            text="Limpar",
            font=("Arial", 10),
            bg="#45475a",
            fg=self.fg_color,
            activebackground="#585b70",
            cursor="hand2",
            padx=20,
            pady=5,
            border=0,
            command=self.limpar
        )
        btn_limpar.pack(side=tk.LEFT, padx=5)
        
        # Botão Copiar
        btn_copiar = tk.Button(
            btn_frame,
            text="Copiar JSON",
            font=("Arial", 10),
            bg="#45475a",
            fg=self.fg_color,
            activebackground="#585b70",
            cursor="hand2",
            padx=20,
            pady=5,
            border=0,
            command=self.copiar_texto
        )
        btn_copiar.pack(side=tk.LEFT, padx=5)
        
        # ========== COLUNA DIREITA ==========
        
        # ===== ÁREA DE RESULTADO =====
        resultado_label = tk.Label(
            right_frame,
            text="Resultado baseado no número de jogos:",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        resultado_label.pack(anchor="w", pady=(0, 5))
        
        # Frame com scroll para cards
        self.resultado_canvas = tk.Canvas(right_frame, bg=self.card_bg, highlightthickness=0)
        resultado_scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.resultado_canvas.yview)
        
        self.cards_frame = tk.Frame(self.resultado_canvas, bg=self.card_bg)
        self.cards_frame.bind("<Configure>", lambda e: self.resultado_canvas.configure(scrollregion=self.resultado_canvas.bbox("all")))
        
        self.resultado_canvas.create_window((0, 0), window=self.cards_frame, anchor="nw")
        self.resultado_canvas.configure(yscrollcommand=resultado_scrollbar.set)
        
        # Scroll com mouse
        def _on_card_mousewheel(event):
            self.resultado_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.resultado_canvas.bind_all("<Button-4>", _on_card_mousewheel)
        self.resultado_canvas.bind_all("<Button-5>", _on_card_mousewheel)
        
        resultado_scrollbar.pack(side="right", fill="y")
        self.resultado_canvas.pack(side="left", fill="both", expand=True)
        
        # Mensagem inicial
        self.msg_inicial = tk.Label(
            self.cards_frame,
            text="Aguardando busca de estatísticas...",
            font=("Arial", 11),
            bg=self.card_bg,
            fg=self.fg_color,
            pady=20
        )
        self.msg_inicial.pack()
        
        # Adicionar scroll ao canvas principal
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Atualizar região de scroll
        self.root.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        
        # Armazenar JSON para copiar
        self.ultimo_json = ""
    
    def criar_card(self, titulo, items, cor_titulo="#24940e"):
        """Cria um card de estatística com alinhamento correto"""
        card = Frame(self.cards_frame, bg="#45475a", relief=tk.RAISED, borderwidth=2)
        card.pack(fill="x", padx=10, pady=5)

    # Título
        Label(card, text=titulo, font=("Arial", 12, "bold"),
            bg="#45475a", fg=cor_titulo, anchor="w").grid(
            row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(8, 5)
    )

    # Configurar colunas
        card.columnconfigure(0, weight=1)  # texto
        card.columnconfigure(1, weight=0)  # valor fixo

    # Itens
        for i, item in enumerate(items, start=1):
            nome = item.get("nome", "")
            valor = item.get("valor", "")

            Label(card, text=f"• {nome}:",
                font=("Arial", 10),
                bg="#45475a",
                fg=self.fg_color,
                anchor="w").grid(
                row=i, column=0, sticky="w", padx=(15, 5), pady=2
            )

            Label(card, text=valor,
                font=("Arial", 10, "bold"),
                bg="#45475a",
                fg="#3aeb2a",
                anchor="e").grid(
                row=i, column=1, sticky="e", padx=(5, 15), pady=2
            )
        
    def formatar_estatisticas(self, json_str):
        """Formata o JSON em cards visuais (novo formato com mandante/visitante/combinação)"""
        try:
            # Limpar cards anteriores
            for widget in self.cards_frame.winfo_children():
                widget.destroy()
            
            # Parse JSON
            dados = json.loads(json_str)
            
            # Verifica se há erro
            if "erro" in dados:
                Label(self.cards_frame, text=f" {dados['erro']}",
                      font=("Arial", 11, "bold"), bg=self.card_bg, fg="#f44336", pady=10).pack()
                
                if "resposta_original" in dados:
                    Label(self.cards_frame, text=dados['resposta_original'], 
                          font=("Consolas", 9), bg=self.card_bg, fg=self.fg_color, 
                          wraplength=450, justify="left", padx=10).pack()
                return
            
            # ========== MANDANTE ==========
            if "mandante" in dados and dados["mandante"]:
                mandante = dados["mandante"]
                items = []
                
                # Gols por tempo (PORCENTAGEM)
                if mandante.get("gols_por_tempo"):
                    pt = mandante["gols_por_tempo"].get("primeiro_tempo_pct")
                    st = mandante["gols_por_tempo"].get("segundo_tempo_pct")
                    if pt is not None:
                        items.append({"nome": "Gols 1º Tempo", "valor": f"{int(pt*100)}%"})
                    if st is not None:
                        items.append({"nome": "Gols 2º Tempo", "valor": f"{int(st*100)}%"})
                
                # Over
                if mandante.get("over"):
                    o15 = mandante["over"].get("over15")
                    o25 = mandante["over"].get("over25")
                    o35 = mandante["over"].get("over35")
                    if o15 is not None:
                        items.append({"nome": "Over 1.5", "valor": f"{int(o15*100)}%"})
                    if o25 is not None:
                        items.append({"nome": "Over 2.5", "valor": f"{int(o25*100)}%"})
                    if o35 is not None:
                        items.append({"nome": "Over 3.5", "valor": f"{int(o35*100)}%"})
                
                # Chutes
                if mandante.get("chutes"):
                    no_gol = mandante["chutes"].get("no_gol")
                    total = mandante["chutes"].get("total")
                    if no_gol is not None:
                        items.append({"nome": "Chutes no Gol", "valor": f"{no_gol}"})
                    if total is not None:
                        items.append({"nome": "Chutes Total", "valor": f"{total}"})
                
                # Escanteios
                if mandante.get("escanteios") is not None:
                    items.append({"nome": "Escanteios", "valor": f"{mandante['escanteios']}"})
                
                # Cartões
                if mandante.get("cartoes"):
                    amarelos = mandante["cartoes"].get("amarelos")
                    vermelhos = mandante["cartoes"].get("vermelhos")
                    total = mandante["cartoes"].get("total")
                    if amarelos is not None:
                        items.append({"nome": "Cartões Amarelos", "valor": f"{amarelos}"})
                    if vermelhos is not None:
                        items.append({"nome": "Cartões Vermelhos", "valor": f"{vermelhos}"})
                    if total is not None:
                        items.append({"nome": "Total Cartões", "valor": f"{total}"})
                
                # Faltas
                if mandante.get("faltas") is not None:
                    items.append({"nome": "Faltas", "valor": f"{mandante['faltas']}"})
                
                if items:
                    self.criar_card("MANDANTE (CASA)", items, "#24940e")
            
            # ========== VISITANTE ==========
            if "visitante" in dados and dados["visitante"]:
                visitante = dados["visitante"]
                items = []
                
                # Gols por tempo (PORCENTAGEM)
                if visitante.get("gols_por_tempo"):
                    pt = visitante["gols_por_tempo"].get("primeiro_tempo_pct")
                    st = visitante["gols_por_tempo"].get("segundo_tempo_pct")
                    if pt is not None:
                        items.append({"nome": "Gols 1º Tempo", "valor": f"{int(pt*100)}%"})
                    if st is not None:
                        items.append({"nome": "Gols 2º Tempo", "valor": f"{int(st*100)}%"})
                
                # Over
                if visitante.get("over"):
                    o15 = visitante["over"].get("over15")
                    o25 = visitante["over"].get("over25")
                    o35 = visitante["over"].get("over35")
                    if o15 is not None:
                        items.append({"nome": "Over 1.5", "valor": f"{int(o15*100)}%"})
                    if o25 is not None:
                        items.append({"nome": "Over 2.5", "valor": f"{int(o25*100)}%"})
                    if o35 is not None:
                        items.append({"nome": "Over 3.5", "valor": f"{int(o35*100)}%"})
                
                # Chutes
                if visitante.get("chutes"):
                    no_gol = visitante["chutes"].get("no_gol")
                    total = visitante["chutes"].get("total")
                    if no_gol is not None:
                        items.append({"nome": "Chutes no Gol", "valor": f"{no_gol}"})
                    if total is not None:
                        items.append({"nome": "Chutes Total", "valor": f"{total}"})
                
                # Escanteios
                if visitante.get("escanteios") is not None:
                    items.append({"nome": "Escanteios", "valor": f"{visitante['escanteios']}"})
                
                # Cartões
                if visitante.get("cartoes"):
                    amarelos = visitante["cartoes"].get("amarelos")
                    vermelhos = visitante["cartoes"].get("vermelhos")
                    total = visitante["cartoes"].get("total")
                    if amarelos is not None:
                        items.append({"nome": "Cartões Amarelos", "valor": f"{amarelos}"})
                    if vermelhos is not None:
                        items.append({"nome": "Cartões Vermelhos", "valor": f"{vermelhos}"})
                    if total is not None:
                        items.append({"nome": "Total Cartões", "valor": f"{total}"})
                
                # Faltas
                if visitante.get("faltas") is not None:
                    items.append({"nome": "Faltas", "valor": f"{visitante['faltas']}"})
                
                if items:
                    self.criar_card("VISITANTE (FORA)", items, "#2196f3")
            
            # ========== COMBINAÇÃO ==========
            if "combinação" in dados and dados["combinação"]:
                comb = dados["combinação"]
                items = []
                
                # Gols por tempo (PORCENTAGEM)
                if comb.get("gols_por_tempo"):
                    pt = comb["gols_por_tempo"].get("primeiro_tempo_pct")
                    st = comb["gols_por_tempo"].get("segundo_tempo_pct")
                    if pt is not None:
                        items.append({"nome": "Gols 1º Tempo", "valor": f"{int(pt*100)}%"})
                    if st is not None:
                        items.append({"nome": "Gols 2º Tempo", "valor": f"{int(st*100)}%"})
                
                # Over
                if comb.get("over"):
                    o15 = comb["over"].get("over15")
                    o25 = comb["over"].get("over25")
                    o35 = comb["over"].get("over35")
                    if o15 is not None:
                        items.append({"nome": "Over 1.5", "valor": f"{int(o15*100)}%"})
                    if o25 is not None:
                        items.append({"nome": "Over 2.5", "valor": f"{int(o25*100)}%"})
                    if o35 is not None:
                        items.append({"nome": "Over 3.5", "valor": f"{int(o35*100)}%"})
                
                # Chutes
                if comb.get("chutes"):
                    no_gol = comb["chutes"].get("no_gol")
                    total = comb["chutes"].get("total")
                    if no_gol is not None:
                        items.append({"nome": "Chutes no Gol", "valor": f"{no_gol}"})
                    if total is not None:
                        items.append({"nome": "Chutes Total", "valor": f"{total}"})
                
                # Escanteios
                if comb.get("escanteios") is not None:
                    items.append({"nome": "Escanteios", "valor": f"{comb['escanteios']}"})
                
                # Cartões
                if comb.get("cartoes") is not None:
                    items.append({"nome": "Total Cartões", "valor": f"{comb['cartoes']}"})
                
                # Faltas
                if comb.get("faltas") is not None:
                    items.append({"nome": "Faltas", "valor": f"{comb['faltas']}"})
                
                if items:
                    self.criar_card(" COMBINAÇÃO (MÉDIA GERAL)", items, "#ff9800")
            
            # ========== FONTE ==========
            if "fonte" in dados and dados["fonte"]:
                fonte_text = Label(
                    self.cards_frame,
                    text=f" Fonte: {dados['fonte']}",
                    font=("Arial", 9),
                    bg=self.card_bg,
                    fg="#888",
                    wraplength=450,
                    justify="left",
                    padx=10,
                    pady=10
                )
                fonte_text.pack()
            
            # Se nenhum dado foi encontrado
            if not any(key in dados for key in ["mandante", "visitante", "combinação"]):
                Label(self.cards_frame, text="Nenhuma estatística disponível",
                      font=("Arial", 11), bg=self.card_bg, fg=self.fg_color, pady=20).pack()
            
        except json.JSONDecodeError as e:
            # Se não for JSON válido
            Label(self.cards_frame, text=" Erro ao processar ",
                  font=("Arial", 11, "bold"), bg=self.card_bg, fg="#f44336", pady=10).pack()
            
            Label(self.cards_frame, text=f"{str(e)}\n\n{json_str[:400]}...", 
                  font=("Consolas", 8), bg=self.card_bg, fg=self.fg_color, 
                  wraplength=450, justify="left", padx=10).pack()
        
        except Exception as e:
            Label(self.cards_frame, text=f"Erro: {str(e)}",
                  font=("Arial", 10), bg=self.card_bg, fg="#f44336", pady=10).pack()
    
    def atualizar_status(self, mensagem):
        """Atualiza a barra de status"""
        self.status_label.config(text=mensagem)
        self.root.update_idletasks()
    
    def validar_selecoes(self):
        """Valida se os campos obrigatórios foram preenchidos"""
        if "Selecione" in self.combo_home.get():
            messagebox.showwarning("Atenção", "Selecione o time da casa")
            return False
        if "Selecione" in self.combo_away.get():
            messagebox.showwarning("Atenção", "Selecione o time visitante")
            return False
        return True
    
    def buscar_thread(self):
        """Executa a busca em uma thread separada"""
        # Coletar valores
        home = self.combo_home.get()
        away = self.combo_away.get()
        league = self.combo_league.get()
        window = self.combo_window.get()
        home_scope = self.combo_home_scope.get()
        away_scope = self.combo_away_scope.get()
        year = self.combo_year.get()
        
        # Criar prompt
        prompt = PROMPT_TEMPLATE.format(
            home=home,
            away=away,
            league=league,
            window=window,
            home_scope=home_scope,
            away_scope=away_scope,
            year=year
        )
        
        # Limpar cards
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
        
        # Mostrar loading
        loading = Label(
            self.cards_frame,
            text=f"⏳ Buscando estatísticas...\n\n{home} vs {away}\n{league}\n\nAguarde...",
            font=("Arial", 11),
            bg=self.card_bg,
            fg=self.fg_color,
            pady=20
        )
        loading.pack()
        
        self.atualizar_status("Buscando dados...")
        
        # Enviar para IA
        resposta = enviar_para_groq(prompt)
        
        # Armazenar JSON
        self.ultimo_json = resposta if resposta else ""
        
        # Formatar resposta
        if resposta and not resposta.startswith("Erro"):
            self.formatar_estatisticas(resposta)
            self.atualizar_status(" Estatísticas obtidas com sucesso!")
        else:
            for widget in self.cards_frame.winfo_children():
                widget.destroy()
            Label(self.cards_frame, text=f"Erro ao buscar:\n\n{resposta}",
                  font=("Arial", 10), bg=self.card_bg, fg="#f44336", pady=20, wraplength=450).pack()
            self.atualizar_status(" Erro ao buscar estatísticas")
        
        self.btn_gerar.config(state=tk.NORMAL, text=" Buscar Estatísticas")
    
    def buscar_estatisticas(self):
        """Inicia o processo de busca"""
        if not self.validar_selecoes():
            return
        
        # Desabilitar botão
        self.btn_gerar.config(state=tk.DISABLED, text=" Buscando...")
        
        # Executar em thread separada
        thread = threading.Thread(target=self.buscar_thread, daemon=True)
        thread.start()
    
    def limpar(self):
        """Limpa os campos"""
        self.combo_home.set("Selecione o time da casa...")
        self.combo_away.set("Selecione o time visitante...")
        self.combo_league.set("Brasileirão Série A")
        self.combo_window.set("10")
        self.combo_home_scope.set("Geral (todos os jogos)")
        self.combo_away_scope.set("Geral (todos os jogos)")
        self.combo_year.set("2026")
        
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
        
        self.msg_inicial = tk.Label(
            self.cards_frame,
            text=" Aguardando busca de estatísticas...",
            font=("Arial", 11),
            bg=self.card_bg,
            fg=self.fg_color,
            pady=20
        )
        self.msg_inicial.pack()
        
        self.ultimo_json = ""
        self.atualizar_status("Pronto para buscar estatísticas! ")
    
    def copiar_texto(self):
        """Copia o JSON para a área de transferência"""
        if self.ultimo_json and "Erro" not in self.ultimo_json:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.ultimo_json)
            self.atualizar_status(" JSON copiado para a área de transferência!")
            messagebox.showinfo("Sucesso", "JSON copiado com sucesso!")
        else:
            messagebox.showwarning("Atenção", "Não há dados para copiar!")
