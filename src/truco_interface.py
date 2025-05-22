import flet as ft
from game_logic import TrucoGame

class truco_interface(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        
        self.start_top = 0
        self.start_left = 0

        self.jogador1_container = ft.Column()
        self.jogador2_container = ft.Column()
        self.manilha_container = ft.Column()

        self.btn_embaralhar = ft.IconButton(icon=ft.Icons.SHUFFLE, on_click=self.atualizar_cartas)
        self.slot = ft.Container(
        width=70, height=100,left=200, top=170, border=ft.border.all(1)
        )

        self.controls = [
            self.jogador1_container, ft.Divider(),
            self.jogador2_container, 
            ft.Divider(), 
            self.manilha_container,
            self.btn_embaralhar
        ]

        self.atualizar_cartas()

    def atualizar_cartas(self, e=None):
        j1, j2, manilha = TrucoGame.embaralhar()

        # self.jogador1_container.controls = [
        #     ft.Text("Jogador 1:"),
        #     ft.Row([
        #         self.criar_carta(c, jogador=1) for c in j1    
        #     ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
        # ]

        self.jogador1_container.controls = [
            ft.Text("Jogador 1:"),
            ft.Stack(
                controls=[
                    *[self.criar_carta(c, jogador=1, index=i) for i, c in enumerate(j1)],
                    self.slot
                ],
                width=500,
                height=300
            )
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
    
    # FUNÇÕES DO DRAG
    
    def place(card, slot):
        card.top = slot.top
        card.left = slot.left

    def bounce_back(game, card):
        card.top = game.start_top
        card.left = game.start_left

    def start_drag(self, e: ft.DragStartEvent):
        self.start_top = e.control.top
        self.start_left = e.control.left

    def drag(self, e: ft.DragUpdateEvent):
        e.control.top = max(0, e.control.top + e.delta_y)
        e.control.left = max(0, e.control.left + e.delta_x)
        e.control.update()

    def drop(self, e: ft.DragEndEvent):
        top_diff = abs(e.control.top - self.slot.top)
        left_diff = abs(e.control.left - self.slot.left)

        if top_diff < 20 and left_diff < 20:
            # Vai pro slot
            e.control.top = self.slot.top
            e.control.left = self.slot.left
        else:
            # Volta para onde estava antes do arrasto
            e.control.top = self.start_top
            e.control.left = self.start_left

        e.control.update()
    
    # FIM DELAS    
    
    def criar_carta(self, carta, jogador, index=0):
        imagem = 'back_cards.png' if jogador == 2 else carta['image']
        
        left_pos = 50 + index * 100  # evita sobreposição
        top_pos = 20

        if jogador == 1:
            return ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.MOVE,
            drag_interval=5,
            on_pan_start=self.start_drag,
            on_pan_update=self.drag,
            on_pan_end=self.drop,
            left=left_pos,
            top=top_pos,
            content=ft.Container(
                content=ft.Image(imagem),
                width=100,
                height=100,
                border_radius=5
            ),
        )
        else:
            return ft.Column([
                # ft.Text(f"{carta['value']} de {carta['suit']}"),
                ft.Image(src=imagem, width=100)
            ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER)