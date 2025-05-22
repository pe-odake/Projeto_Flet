import requests

class TrucoGame:
    @staticmethod
    def embaralhar():
        truco_cards = [
            'AS','2S','3S','4S','5S','6S','7S','QS','JS','KS',
            'AH','2H','3H','4H','5H','6H','7H','QH','JH','KH',
            'AD','2D','3D','4D','5D','6D','7D','QD','JD','KD',
            'AC','2C','3C','4C','5C','6C','7C','QC','JC','KC'
        ]

        cards_str = ",".join(truco_cards)
        url_create = f"https://deckofcardsapi.com/api/deck/new/shuffle/?cards={cards_str}"
        response_create = requests.get(url_create).json()

        if response_create["success"]:
            deck_id = response_create["deck_id"]
            url_draw = f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=7"
            response_draw = requests.get(url_draw).json()

            if response_draw["success"]:
                cartas = response_draw["cards"]
                jogador1 = cartas[:3]
                jogador2 = cartas[3:6]
                manilha = cartas[6]
                return jogador1, jogador2, manilha

        return [], [], None