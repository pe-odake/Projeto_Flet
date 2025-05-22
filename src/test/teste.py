import flet as ft

class Solitaire:
    def __init__(self):
        self.start_top = 0
        self.start_left = 0

def main(page: ft.Page):
    page.title = "Slot + Voltar ao Original se Retornar"

    solitaire = Solitaire()

    def place(card, slot):
        card.top = slot.top
        card.left = slot.left

    def bounce_back(game, card):
        card.top = game.start_top
        card.left = game.start_left

    def start_drag(e: ft.DragStartEvent):
        # Sempre que a carta for arrastada, salva a posição original (real, atual)
        # assim, se ela estiver no slot, passa a ser o novo "original"
        solitaire.start_top = e.control.top
        solitaire.start_left = e.control.left

    def drag(e: ft.DragUpdateEvent):
        e.control.top = max(0, e.control.top + e.delta_y)
        e.control.left = max(0, e.control.left + e.delta_x)
        e.control.update()

    def drop(e: ft.DragEndEvent):
        top_diff = abs(e.control.top - slot.top)
        left_diff = abs(e.control.left - slot.left)

        original_diff_top = abs(e.control.top - 50)   # coordenada original fixa
        original_diff_left = abs(e.control.left - 50)

        if top_diff < 20 and left_diff < 20:
            # Vai pro slot
            place(e.control, slot)

        elif original_diff_top < 20 and original_diff_left < 20:
            # Volta manual pro local original (50, 50)
            e.control.top = 50
            e.control.left = 50

        else:
            # Caso contrário, volta de onde saiu
            bounce_back(solitaire, e.control)

        e.control.update()

    # Slot (destino)
    slot = ft.Container(
        width=70,
        height=150,
        left=200,
        top=100,
        border=ft.border.all(2, ft.Colors.BLACK),
        bgcolor=ft.Colors.GREY_200
    )

    # Base azul (local original)
    original_slot = ft.Container(
        width=100,
        height=100,
        left=50,
        top=50,
        border=ft.border.all(2, ft.Colors.BLUE),
        bgcolor=ft.Colors.BLUE_100
    )

    # Carta
    card = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=5,
        on_pan_start=start_drag,
        on_pan_update=drag,
        on_pan_end=drop,
        left=50,
        top=50,
        content=ft.Container(
            content=ft.Image(src='../coco.png'),
            width=70,
            height=100,
            border_radius=10
        ),
    )

    page.add(
        ft.Stack(
            controls=[slot, original_slot, card],
            width=500,
            height=300
        )
    )

ft.app(target=main, assets_dir="assets")