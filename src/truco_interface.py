import flet as ft
from game_logic import TrucoGame

class truco_interface(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        self.jogador1_container = ft.Column()
        self.jogador2_container = ft.Column()
        self.manilha_container = ft.Column()

        self.btn_embaralhar = ft.IconButton(icon=ft.Icons.SHUFFLE, on_click=self.atualizar_cartas)

        self.controls = [
            self.jogador1_container, ft.Divider(),
            self.jogador2_container, ft.Divider(),
            self.manilha_container, ft.Divider(),
            self.btn_embaralhar
        ]

        self.atualizar_cartas()

    def atualizar_cartas(self, e=None):
        j1, j2, manilha = TrucoGame.embaralhar()

        self.jogador1_container.controls = [
            ft.Text("Jogador 1:"),
            ft.Row([
                self.criar_carta(c, jogador=1) for c in j1
            ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
        ]

        self.jogador2_container.controls = [
            ft.Text("Jogador 2:"),
            ft.Row([
                self.criar_carta(c, jogador=2) for c in j2
            ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
        ]

        self.manilha_container.controls = [
            ft.Text("Manilha:"),
            ft.Image(src=manilha['image'], width=120) if manilha else ft.Text("Erro")
        ]

        self.page.update()

    def criar_carta(self, carta, jogador):
        imagem = 'back_cards.png' if jogador == 2 else carta['image']
        
        return ft.Column([
            ft.Text(f"{carta['value']} de {carta['suit']}"),
            ft.Image(src=imagem, width=100)
        ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER)