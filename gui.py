from config import GROQ_API_KEY, GROQ_API_URL, GROQ_MODEL
import tkinter as tk
from tkinter import Tk,scrolledtext, messagebox,ttk
from constants import TIMES_BRASILEIROS, COMPETICOES, JANELAS, SCOPES, ANOS, PROMPT_TEMPLATE
from api_client import enviar_para_groq, formatar_json
import requests
import threading
 
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
            text="Resultado:",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        resultado_label.pack(anchor="w", pady=(0, 5))
        
        # Área de texto com scroll
        self.text_resultado = scrolledtext.ScrolledText(
            right_frame,
            wrap=tk.WORD,
            font=("Consolas", 9),
            bg="#313244",
            fg="#3aeb2a",
            insertbackground=self.fg_color,
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.text_resultado.pack(fill="both", expand=True)
        self.text_resultado.insert("1.0", "Aguardando busca de estatísticas... ")
        self.text_resultado.config(state=tk.DISABLED)
        
        # Adicionar scroll ao canvas (DEPOIS do status bar)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Atualizar região de scroll
        self.root.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    def atualizar_status(self, mensagem):
        """Atualiza a barra de status"""
        self.status_label.config(text=mensagem)
        self.root.update_idletasks()
    
    def validar_selecoes(self):
        """Valida se os campos obrigatórios foram preenchidos"""
        if "Selecione" in self.combo_home.get():
            messagebox.showwarning("Atenção", "Selecione")
            return False
        if "Selecione" in self.combo_away.get():
            messagebox.showwarning("Atenção", "Selecione")
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
        
        # Atualizar interface
        self.text_resultado.config(state=tk.NORMAL)
        self.text_resultado.delete("1.0", tk.END)
        self.text_resultado.insert("1.0", 
            f" Buscando estatísticas...\n"
            f" {home} vs {away}\n"
            f" {league}\n"
            f" Aguarde, isso pode levar alguns segundos...\n"
        )
        self.text_resultado.config(state=tk.DISABLED)
        self.atualizar_status(" Conectando com a IA e buscando dados...")
        
        # Enviar para IA
        resposta = enviar_para_groq(prompt)
        
        # Formatar resposta
        resposta_formatada = formatar_json(resposta) if resposta else "Erro ao buscar"
        
        # Atualizar resultado
        self.text_resultado.config(state=tk.NORMAL)
        self.text_resultado.delete("1.0", tk.END)
        
        if resposta and not resposta.startswith("Erro"):
            self.text_resultado.insert("1.0", resposta_formatada)
            self.atualizar_status(" Estatísticas obtidas com sucesso!")
        else:
            self.text_resultado.insert("1.0", f" Erro:\n\n{resposta}")
            self.atualizar_status(" Erro ao buscar estatísticas")
        
        self.text_resultado.config(state=tk.DISABLED)
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
        
        self.text_resultado.config(state=tk.NORMAL)
        self.text_resultado.delete("1.0", tk.END)
        self.text_resultado.insert("1.0", "Aguardando busca de estatísticas... ")
        self.text_resultado.config(state=tk.DISABLED)
        self.atualizar_status("Pronto para buscar estatísticas! ")
    
    def copiar_texto(self):
        """Copia o JSON para a área de transferência"""
        texto = self.text_resultado.get("1.0", tk.END).strip()
        if texto and "Aguardando" not in texto:
            self.root.clipboard_clear()
            self.root.clipboard_append(texto)
            self.atualizar_status(" JSON copiado para a área de transferência!")
            messagebox.showinfo("Sucesso", "JSON copiado com sucesso!")
        else:
            messagebox.showwarning("Atenção", "Não há dados para copiar!")
