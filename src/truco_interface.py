import flet as ft
from game_logic import TrucoGame

class truco_interface(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        
        self.start_top = 0
        self.start_left = 0
        
        self.cartas_no_slot_jogada = []
        
        self.jogador1_container = ft.Column()
        self.jogador2_container = ft.Column()
        self.manilha_container = ft.Column()

        self.cartas_jogador1 = []
        self.cartas_jogador2 = []  # Lista de cartas do jogador 2

        self.slot_jogada2 = ft.Row(
            controls=[],
            alignment=ft.MainAxisAlignment.CENTER
        )

        self.manilha = ft.Container()  # Container que armazenará a imagem da manilha

        self.btn_embaralhar = ft.IconButton(icon=ft.Icons.SHUFFLE, on_click=self.atualizar_cartas)
        self.slot = ft.Container(
                width=70,
                height=100,
                left=200,
                top=170,
                border=ft.border.all(2),
                border_radius=5
        )

        self.slot_jogada = ft.Container(
                width=70,
                height=100,
                left=150,
                top=300,
                border=ft.border.all(2),
                border_radius=5
        )

        self.btn_confirmar_jogada = ft.ElevatedButton(
            text="Confirmar Jogada",
            on_click=self.confirmar_jogada
        )

        self.controls = [
            self.jogador1_container, ft.Divider(),
            self.btn_confirmar_jogada,
            self.slot_jogada2,
            self.jogador2_container, 
            ft.Divider(), 
            self.manilha_container,
            self.btn_embaralhar
        ]

        self.atualizar_cartas()

    def atualizar_cartas(self, e=None):
        j1, j2, manilha = TrucoGame.embaralhar()

        self.cartas_jogador2 = j2  # <-- ADICIONE ISSO!

        self.cartas_no_slot_jogada.clear()  # limpa o slot
        self.cartas_jogador1.clear()  # limpa a lista de cartas

        slots_cartas = [self.criar_carta(c, jogador=1, index=i) for i, c in enumerate(j1)]
        slots = [item[0] for item in slots_cartas]
        cartas = [item[1] for item in slots_cartas]

        # Salva as cartas do jogador 1
        self.cartas_jogador1 = cartas

        # Atualiza a interface do jogador 1 com Stack (slots + cartas + slot de jogada)
        self.jogador1_container.controls = [
            ft.Text("Jogador 1:"),
            ft.Stack(
                controls=[*slots, *cartas, self.slot_jogada],
                width=600,
                height=400
            )
        ]

        # Atualiza a interface do jogador 2
        self.jogador2_container.controls = [
            ft.Text("Jogador 2:"),
            ft.Row([
                self.criar_carta(c, jogador=2) for c in j2
            ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
        ]

        # Atualiza a manilha
        self.manilha_container.controls = [
            ft.Text("Manilha:"),
            ft.Image(src=manilha['image'], width=120, data=manilha) if manilha else ft.Text("Erro")
        ]

        self.manilha.content = ft.Image(src=manilha['image'], width=120)
        self.manilha.data = manilha

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
        def is_in_slot(slot):
            return abs(e.control.top - slot.top) < 20 and abs(e.control.left - slot.left) < 20

        stack_cartas = self.jogador1_container.controls[1]  # O Stack com cartas + slots

        if is_in_slot(self.slot_jogada):
            # Remove carta anterior do slot se existir
            if self.cartas_no_slot_jogada:
                carta_antiga = self.cartas_no_slot_jogada.pop()
                slot_antigo = carta_antiga.data["slot"]
                slot_antigo.visible = True
                carta_antiga.top = carta_antiga.data["original_top"]
                carta_antiga.left = carta_antiga.data["original_left"]
                stack_cartas.controls.append(carta_antiga)
                self.cartas_jogador1.append(carta_antiga)

            # Posiciona nova carta
            e.control.top = self.slot_jogada.top
            e.control.left = self.slot_jogada.left

            # Esconde slot da carta jogada
            slot_atual = e.control.data["slot"]
            slot_atual.visible = False

            if e.control not in stack_cartas.controls:
                stack_cartas.controls.append(e.control)

            self.cartas_no_slot_jogada.append(e.control)

            if e.control in self.cartas_jogador1:
                self.cartas_jogador1.remove(e.control)

        else:
            # Volta para posição original
            e.control.top = e.control.data["original_top"]
            e.control.left = e.control.data["original_left"]

            slot = e.control.data["slot"]
            slot.visible = True  # Reexibe o slot

            if e.control not in stack_cartas.controls:
                stack_cartas.controls.append(e.control)

            if e.control not in self.cartas_jogador1:
                self.cartas_jogador1.append(e.control)

        e.control.update()
        self.page.update()


    
    # FIM DELAS    
    
    def criar_carta(self, carta, jogador, index=0):
        imagem = 'back_cards.png' if jogador == 2 else carta['image']
        
        left_pos = 50 + index * 100  # evita sobreposição
        top_pos = 170

        if jogador == 1:
            slot = ft.Container(
                width=70,
                height=100,
                left=left_pos,
                top=top_pos,
                border=ft.border.all(2, ft.Colors.BLUE),
                border_radius=5
            )

            carta_widget = ft.GestureDetector(
                mouse_cursor=ft.MouseCursor.MOVE,
                drag_interval=5,
                on_pan_start=self.start_drag,
                on_pan_update=self.drag,
                on_pan_end=self.drop,
                left=left_pos,
                top=top_pos,
                data={"original_top": top_pos, "original_left": left_pos, "slot": slot},  # <- salva o slot
                content=ft.Container(
                    content=ft.Image(imagem),
                    width=70,
                    height=100,
                    border_radius=5
                ),
            )


            return (slot, carta_widget)

        
        else:
            return ft.Column([
                ft.Image(src=imagem, width=100)
            ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

# CONFIRMAR JOGADA

    def confirmar_jogada(self, e):
        if not self.cartas_no_slot_jogada:
            self.page.snack_bar = ft.SnackBar(ft.Text("Jogador 1 precisa jogar uma carta."))
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Jogador 2 joga automaticamente a primeira carta da mão
        if not self.slot_jogada2.controls:
            primeira_carta_j2 = self.cartas_jogador2[0]
            self.cartas_jogador2.remove(primeira_carta_j2)
            self.slot_jogada2.controls.append(
                ft.Image(src=primeira_carta_j2['image'], width=100, data=primeira_carta_j2)
            )
            self.slot_jogada2.update()

        carta1 = self.get_card_info(self.cartas_no_slot_jogada[0])
        carta2 = self.slot_jogada2.controls[0].data
        manilha_base = self.manilha.data

        vencedor = TrucoGame.comparar_cartas(carta1, carta2, manilha_base)

        if vencedor == 1:
            resultado = "Jogador 1 venceu a rodada!"
        elif vencedor == 2:
            resultado = "Jogador 2 venceu a rodada!"
        else:
            resultado = "Empate na rodada!"

        print(f"Resultado: {resultado}")
        print(f"Jogador 1 jogou: {carta1['value']}")
        print(f"Jogador 2 jogou: {carta2['value']}")
        print(f"Manilha: {manilha_base['value']}")

        self.page.snack_bar = ft.SnackBar(ft.Text(resultado))
        self.page.snack_bar.open = True
        self.page.update()



    def get_card_info(self, carta_widget):
        image_src = carta_widget.content.content.src  # Acessa ft.Image.src
        nome_arquivo = image_src.split('/')[-1].split('.')[0]  # Ex: '4H'
        return {
            'code': nome_arquivo,
            'value': nome_arquivo[:-1],
            'suit': nome_arquivo[-1]
        }
