import random

suits = ('Червы', 'Бубны', 'Пики', 'Трефы')
ranks = ('Двойка', 'Тройка', 'Четвёрка', 'Пятерка', 'Шестёрка', 'Семёрка',
         'Восьмёрка', 'Девятка', 'Десятка', 'Валет', 'Дама', 'Король', 'Туз')
values = {
    'Двойка': 2,
    'Тройка': 3,
    'Четвёрка': 4,
    'Пятерка': 5,
    'Шестёрка': 6,
    'Семёрка': 7,
    'Восьмёрка': 8,
    'Девятка': 9,
    'Десятка': 10,
    'Валет': 10,
    'Дама': 10,
    'Король': 10,
    'Туз': 11
}

playing = True


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f'{self.rank} {self.suit}'


class Deck:

    def __init__(self):
        self.deck = []  # начинаем с пустого списка
        for suit in suits:
            for rank in ranks:
                self.deck.append(f'{rank} {suit}')

    def __str__(self):
        deck = ""
        for card in self.deck:
            deck += card.__str__() + '\n'
        return deck

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand:

    def __init__(self):
        self.cards = [
        ]  # начинаем с пустого списка, так же, как и в классе Deck
        self.value = 0  # начинаем со значения 0
        self.aces = 0  # добавляем атрибут, чтобы учитывать тузы

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Туз':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:

    def __init__(self, total=100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet
