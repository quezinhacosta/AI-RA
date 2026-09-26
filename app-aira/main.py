import os
import flet as ft
from dotenv import load_dotenv
import flet

# Carrega as variáveis de ambiente (.env)
load_dotenv()

# Importações dos módulos internos do projeto
from src.ui.theme import AppTheme
from src.ui.components.sidebar import SidebarComponent
from src.ui.components.spotlight import GoalSpotlightComponent
from src.ui.components.metrics import MetricsVisualizerComponent
from src.ui.components.chat import ChatStreamComponent
from src.storage import StorageService
from src.groq_service import GroqService
from src.prompt_engine import PromptEngine



def main(page: ft.Page):
    # 1. Configurações da Janela Nativa Desktop
    page.title = "AI-RA • Seu Copiloto Pessoal"
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 980
    page.window.min_height = 680
    page.window.center_on_init = True
    page.padding = 24
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # 2. Inicialização dos Serviços (Storage, Groq, Prompts)
    storage = StorageService()
    user_state = storage.load_user_state()
    groq_service = GroqService(api_key=os.getenv("GROQ_API_KEY"))
    prompt_engine = PromptEngine(user_state=user_state)

    # 3. Instanciação dos Componentes Visuais (100% Python)
    sidebar = SidebarComponent(user_name=user_state.get("profile", {}).get("name", "Quezia"))
    spotlight = GoalSpotlightComponent(primary_goal=user_state.get("primary_goals", {}).get("financial", {}))
    metrics = MetricsVisualizerComponent(state=user_state)
    chat = ChatStreamComponent(groq_service=groq_service, prompt_engine=prompt_engine, storage=storage)

    # 4. Painel Central/Direito (Dashboard Superior + Área de Chat Inferior)
    main_dashboard = ft.Container(
        expand=True,
        content=ft.Column(
            expand=True,
            spacing=18,
            controls=[
                # Linha Superior: Cartão de Destaque da Meta + Cartão de Métricas
                ft.Row(
                    spacing=18,
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        spotlight,   # Cartão da Meta do Apartamento
                        metrics      # Cartão de Métricas e Progresso
                    ]
                ),
                # Linha Inferior: Painel de Conversa com a IA
                ft.Container(
                    expand=True,
                    bgcolor=AppTheme.CARD_BG,
                    border_radius=28,
                    padding=20,
                    shadow=AppTheme.SOFT_SHADOW,
                    content=chat     # Feed e input de mensagens
                )
            ]
        )
    )

    # 5. Estrutura Base com Fundo Gradiente Suave (Soft UI)
    app_layout = ft.Container(
        expand=True,
        border_radius=32,
        padding=16,
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
            colors=[AppTheme.BG_GRADIENT_START, AppTheme.BG_GRADIENT_END]
        ),
        content=ft.Row(
            expand=True,
            spacing=20,
            controls=[
                sidebar,        # Barra lateral translúcida à esquerda
                main_dashboard  # Painel principal à direita
            ]
        )
    )

    # Adiciona a estrutura completa à janela
    page.add(app_layout)


if __name__ == "__main__":
    if hasattr(ft, "app"):
        ft.app(main)
    elif hasattr(ft, "run"):
        ft.run(main)
    else:
        flet.app(target=main)