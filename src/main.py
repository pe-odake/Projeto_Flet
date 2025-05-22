import flet as ft
from truco_interface import truco_interface

def main(page: ft.Page):
    page.title = "Truco"
    page.scroll = True
    page.add(truco_interface(page))

ft.app(target=main)
