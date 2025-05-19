import flet as ft
from inicio_rota_page import menu_view
from rota_teste1 import game_view

def main(page: ft.Page):
    page.title = "Jogo de Truco"

    def route_change(route):
        page.views.clear()
        
        if page.route == "/":
            page.views.append(menu_view(page))  # Tela de menu
        elif page.route == "/jogo":
            page.views.append(game_view(page))  # Tela do jogo

        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main, assets_dir="assets")
