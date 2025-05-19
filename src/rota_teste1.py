import flet as ft

def game_view(page: ft.Page):
    return ft.View(
        route="/jogo", # <--- ENDEREÇO DESSA PAGINA
        controls=[
            ft.Text("Página do Jogo", size=24),
            ft.ElevatedButton("ABACAXI", on_click=lambda e: page.go("/")), # <--- ROTA QUE ESTA VOLTANDO UMA ATRAS
            ft.Image(src='abacaxi.png', width=120)
        ]
    )
