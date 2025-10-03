import customtkinter
import logica_agente as logica # Importa nosso arquivo de lógica

# Configurações da aparência
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Agente de Investimentos Pessoal")
        self.geometry("800x600")

        # Carregar dados e configurar IA no início
        self.carteira = logica.carregar_carteira()
        try:
            self.modelo_ia = logica.configurar_ia()
        except ValueError as e:
            # Em uma app real, mostraríamos um popup de erro
            print(e)
            exit()

        # --- Layout da Janela ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Frame dos botões (menu lateral)
        self.frame_menu = customtkinter.CTkFrame(self, width=180, corner_radius=0)
        self.frame_menu.grid(row=0, column=0, sticky="nswe")
        
        # Caixa de texto para exibir os resultados
        self.textbox_resultado = customtkinter.CTkTextbox(self, state="disabled", wrap="word")
        self.textbox_resultado.grid(row=0, column=1, padx=20, pady=20, sticky="nswe")
        
        # --- Botões do Menu ---
        self.label_titulo = customtkinter.CTkLabel(self.frame_menu, text="Menu Principal", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_titulo.pack(pady=20, padx=20)

        self.btn_visualizar = customtkinter.CTkButton(self.frame_menu, text="Visualizar Carteira", command=self.visualizar_carteira_gui)
        self.btn_visualizar.pack(pady=10, padx=20, fill="x")
        
        self.btn_adicionar = customtkinter.CTkButton(self.frame_menu, text="Adicionar Ativo", command=self.adicionar_ativo_gui)
        self.btn_adicionar.pack(pady=10, padx=20, fill="x")

        self.btn_remover = customtkinter.CTkButton(self.frame_menu, text="Remover Ativo", command=self.remover_ativo_gui)
        self.btn_remover.pack(pady=10, padx=20, fill="x")

        self.btn_analisar = customtkinter.CTkButton(self.frame_menu, text="Analisar Notícias", command=self.analisar_noticias_gui)
        self.btn_analisar.pack(pady=10, padx=20, fill="x")

        # Configurar o salvamento ao fechar a janela
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)

        # Exibir a carteira ao iniciar
        self.visualizar_carteira_gui()

    # --- Funções que Conectam Botões à Lógica ---

    def atualizar_textbox(self, texto):
        """Função para limpar e escrever na caixa de texto."""
        self.textbox_resultado.configure(state="normal")
        self.textbox_resultado.delete("1.0", "end")
        self.textbox_resultado.insert("1.0", texto)
        self.textbox_resultado.configure(state="disabled")

    def visualizar_carteira_gui(self):
        texto_carteira = logica.formatar_carteira_para_texto(self.carteira)
        self.atualizar_textbox(texto_carteira)

    def adicionar_ativo_gui(self):
        # Cria uma caixa de diálogo para pegar o ticker
        dialog_ticker = customtkinter.CTkInputDialog(text="Digite o ticker do ativo:", title="Adicionar Ativo")
        ticker = dialog_ticker.get_input()
        if not ticker: return # Usuário cancelou
        
        # Cria uma caixa de diálogo para pegar a quantidade
        dialog_qtd = customtkinter.CTkInputDialog(text=f"Digite a quantidade de {ticker.upper()}:", title="Adicionar Ativo")
        qtd_str = dialog_qtd.get_input()
        if not qtd_str: return
        
        # Cria uma caixa de diálogo para pegar o preço médio
        dialog_pm = customtkinter.CTkInputDialog(text=f"Digite o preço médio para {ticker.upper()}:", title="Adicionar Ativo")
        pm_str = dialog_pm.get_input()
        if not pm_str: return

        try:
            self.carteira[ticker.upper()] = {
                "quantidade": int(qtd_str),
                "preco_medio": float(pm_str)
            }
            self.atualizar_textbox(f"Ativo {ticker.upper()} adicionado/atualizado!\n\n" + logica.formatar_carteira_para_texto(self.carteira))
        except ValueError:
            self.atualizar_textbox("ERRO: Quantidade e preço devem ser números.")

    def remover_ativo_gui(self):
        dialog_ticker = customtkinter.CTkInputDialog(text="Qual ticker deseja remover?", title="Remover Ativo")
        ticker = dialog_ticker.get_input()
        if not ticker: return

        if ticker.upper() in self.carteira:
            del self.carteira[ticker.upper()]
            self.atualizar_textbox(f"Ativo {ticker.upper()} removido!\n\n" + logica.formatar_carteira_para_texto(self.carteira))
        else:
            self.atualizar_textbox(f"ERRO: Ativo {ticker.upper()} não encontrado.")

    def analisar_noticias_gui(self):
        self.atualizar_textbox("Analisando notícias... Isso pode levar um momento.")
        self.update_idletasks() # Força a atualização da UI
        
        resultado_analise = logica.analisar_noticias_relevantes(self.carteira, self.modelo_ia)
        self.atualizar_textbox(resultado_analise)

    def fechar_janela(self):
        """Salva a carteira antes de fechar o app."""
        logica.salvar_carteira(self.carteira)
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()