from ast import While
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
                self.deck.append(Card(suit, rank))

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
        self.cards = []
        self.value = 0
        self.aces = 0

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


def take_bet(chips):
    while True:
        try:
            print(f'Ваш баланс равен {chips.total} монет')
            chips.bet = int(input('Введите вашу ставку: '))
        except:
            print('Ставка должна быть числом, повторите ввод')
            continue
        else:
            if (chips.bet > chips.total):
                print(f'Ваша ставка превышает баланс, {chips.total}')
            else:
                break


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing  # для контроля цикла while

    while True:
        answer = input(
            'Вы желаете взять дополнительную карту? Введите Y для согласия или N для того, чтобы остаться при своих картах. '
        )

        if answer.upper() == 'Y':
            hit(deck, hand)  # определённая выше функция hit()

        elif answer.upper() == 'N':
            print("Игрок остается при текущих картах. Ход дилера.")
            playing = False

        else:
            print("Некорректный ввод.")
            continue
        break


def show_some(player, dealer):
    print("\nКарты Дилера:")
    print(" <карта скрыта>")
    print('', dealer.cards[1])
    print("\nКарты Игрока:", *player.cards, sep='\n ')


def show_all(player, dealer):
    print("\nКарты Дилера:", *dealer.cards, sep='\n ')
    print("Карты Дилера =", dealer.value)
    print("\nКарты Игрока:", *player.cards, sep='\n ')
    print("Карты Игрока =", player.value)


def player_busts(chips):
    print("Игрок превысил 21!")
    chips.lose_bet()


def player_wins(chips):
    print("Игрок выиграл!")
    chips.win_bet()


def dealer_busts(chips):
    print("Дилер превысил 21!")
    chips.win_bet()


def dealer_wins(chips):
    print("Дилер выиграл!")
    chips.lose_bet()


def draw():
    print("Ничья!.")


while True:
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    player_chips = Chips()

    take_bet(player_chips)

    show_some(player_hand, dealer_hand)

    while playing:

        hit_or_stand(deck, player_hand)

        show_some(player_hand, dealer_hand)

        if player_hand.value > 21:
            player_busts(player_chips)
            show_all(player_hand, dealer_hand)
            break

    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        show_all(player_hand, dealer_hand)

        if dealer_hand.value > 21:
            dealer_busts(player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_chips)

        else:
            draw()

    print("\nСумма фишек Игрока - ", player_chips.total)

    new_game = input("Хотите ли сыграть снова? Введите 'Y' или 'N' ")
    if new_game[0].upper() == 'Y':
        playing = True
        continue
    else:
        break
