import random
from copy import deepcopy
from multiprocessing import Pool

comb_name_dict = {
    0: 'HighCard',
    1: 'Pair',
    2: 'TwoPairs',
    3: 'Set',
    4: 'Straight',
    5: 'Flush',
    6: 'FullHouse',
    7: 'Four',
    8: 'StraightFlush',
    9: 'FlushRoyal'
    }

any_suit_const = 9

class PokerError(Exception):
    def __init__(self, text='', value=-1):
        self.text = text
        self.value = value

    def __str__(self):
        return f'{self.text} Err no. {self.value}'


class Suit:
    """
    ['s', 'h', 'c', 'd', '*']
    Suit(int), example: Suit(0) = s
    Suit(str), example: Suit('h'), Suit('hearts')
    """

    def __init__(self, x):
        sd = {'s': 0, 'h': 1, 'c': 2, 'd': 3, '*': -1}
        sdl = ['spades', 'hearts', 'clubs', 'diamonds']

        if type(x) == int and x in range(-1, 4):
            self.int = x

        elif type(x) == str and len(x) == 1:
            self.int = sd[x]

        elif type(x) == str and len(x) > 1:
            self.int = sdl.index(x)

        elif type(x) == type(self):
            self.int = x.int

        else:
            raise PokerError(f'{x} - it\'s not a card\'s suit')

    def __repr__(self, short=True):
        sdl = ['spades', 'hearts', 'clubs', 'diamonds']
        sdt = ['s', 'h', 'c', 'd', '*']
        return sdt[self.int] if short else sdl[self.int]

    __str__ = __repr__

    def __eq__(self, other):
        return self.int == other.int or self.int == -1 or other.int == -1

    def get_int(self):
        return self.int


class Number:
    """
    Number(int), example: Number(10) <=> Q
    Number(str), example: Number('Q')
    """
    def __init__(self, x):
        nd = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, 'T': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12}

        if type(x) == str and x in nd:
            self.int = nd[x]

        elif type(x) == int and x in range(13):
            self.int = x

        elif type(x) == type(self):
            self.int = x.int

        else:
            raise PokerError (f'{x} ({type(x)}) - it\'s not a card\'s number')

    def __repr__(self):
        ndt = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        return ndt[self.int]

    __str__ = __repr__

    def __add__(self, x):
        return type(self)((self.int + x) % 13)

    def __sub__(self, x):
        return type(self)((self.int - x) % 13)

    def __eq__(self, other):
        return self.int == other.int

    def __gt__(self, other):
        return self.int > other.int

    def __lt__(self, other):
        return self.int < other.int

    def get_int(self):
        return self.int

class Card:
    def __init__(self, x=None, y=None):
        nd = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, 'T': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12}
        sd = {'s': 0, 'h': 1, 'c': 2, 'd': 3, '*': -1}
        x_not_a_card_error =  f'{x} - it\'s not a card.'
        x_y_not_a_card_error = f'({x}, {y}) - it\'s not a card.'

        if isinstance(x, Number) and isinstance(y, Suit):
            self.number = x
            self.suit = y

        else:
            if x is not None and y is None:
                if type(x) == int:  # example: card(47)
                    if x in range(52):
                        S = x // 13
                        N = x % 13
                    else:
                        raise PokerError(f'{x} out of range. The card number must be in [0 - 52).')

                elif type(x) == str:
                    if len(x) > 3:  # example: Card('T of diamonds')
                        x = x.split()
                        n = x[0][0]
                        s = x[-1][0]
                    elif len(x) == 2:  # example: Card('Td')
                        n = x[0]
                        s = x[-1]
                    elif len(x) == 1:  # example: Card('A')
                        n = x
                        s = '*'
                    else:
                        raise PokerError(x_not_a_card_error)

                    if n in nd.keys() and s in sd.keys():
                        N = nd[n]
                        S = sd[s]
                    else:
                        raise PokerError(x_not_a_card_error)

                elif type(x) == type(self):
                    S = x.suit
                    N = x.number

            elif type(y) == str:
                S = sd[y]

                if type(x) == str and x in nd.keys():  # example Card('T', 'd')
                    N = nd[x]
                elif type(x) == int and x in nd.values():  # example Card(12, 'd')
                    N = x
                else:
                    raise PokerError(x_y_not_a_card_error)

            else:
                raise PokerError(x_y_not_a_card_error)

            self.suit = Suit(S)
            self.number = Number(N)

            self.weight = (self.get_number_int() + 1) * 100 + self.get_suit_int()
            if self.get_suit_int() < 0:
                self.weight = (self.get_number_int() + 1) * 100 + any_suit_const

    def show(self, short=False):
        sdt = ['s', 'h', 'c', 'd', '*']
        sdl = ['spades', 'hearts', 'clubs', 'diamonds']
        ndt = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

        return f'{self.number}{"" if short else " of "}{self.suit.__repr__(short)}'

    def get_color(self):
        if self.get_suit_int() in [1, 3]:
            return 'red'

        return 'black'

    def get_suit_int(self):
        return self.suit.get_int()

    def get_number_int(self):
        return self.number.get_int()

    def get_weight(self):
        return self.weight

    def get_card_in_deck_num(self):
        return self.get_number_int() + self.get_suit_int() * 13

    def __repr__(self):
        return self.show(short=True)

    __str__ = __repr__

    def __add__(self, digit):
        if type(digit) == int:
            return Card(self.number + digit, Suit('*'))

        raise PokerError(f'Can\'t add {digit} ({type(digit)}) to card')

    def __sub__(self, digit):
        if type(digit) == int:
            return Card(self.number - digit, Suit('*'))

        raise PokerError(f'Can\'t substract {digit} ({type(digit)}) from card')

    def __getitem__(self, i):
        return self

    def __eq__(self, other):
        return self.number == other.number and self.suit == other.suit

    def __gt__(self, other):
        return self.get_weight() > other.get_weight()
        # return self.number > other.number

    def __lt__(self, other):
        return self.get_weight() < other.get_weight()
        # return self.number < other.number

    def __ge__(self, other):
        return self > other or self == other

    def __le__(self, other):
        return self < other or self == other


class Deck:
    def __init__(self, cardlist, now_check=True):
        if type(cardlist) == str:
            cardlist = [Card(c) for c in cardlist.split(',')]

        elif type(cardlist) == list and all([isinstance(c, Card) for c in cardlist]):
            pass

        elif type(cardlist) == list and all([type(c) == str for c in cardlist]):
            cardlist = [Card(c) for c in cardlist]

        elif type(cardlist) == list and all([isinstance(c, int) for c in cardlist]):
            cardlist = [Card(c) for c in cardlist]

        else:
            raise PokerError(f'{cardlist}({type(cardlist)}) - it\'s not a deck!')

        cardlist.sort()
        self.is_flush = False  # Наличие флеша
        self._len = len(cardlist)
        self.cards = []  # Все карты деки обьектами
        self.suits = [0, 0, 0, 0] # Количество карт каждой масти (suit)
        self.numbers = []  # Список уникальных значений (number) карт в деке
        self.nn = []  # Количество значений (number) каждой карты

        for card in cardlist:
            self.cards.append(card)
            tc = Card(card.number, Suit('*'))

            if tc not in self.numbers:
                self.numbers.append(tc)
                self.nn.append(1)
            else:
                self.nn[self.numbers.index(tc)] += 1

            if card.get_suit_int() >= 0:
                self.suits[card.get_suit_int()] += 1
            else:
                for i in self.suits:
                    i += 1

        self.ncards = []

        for card in self.cards:
            self.ncards.append(self.nn[self.numbers.index(card)])

        # Количество разных карт
        self.lenu = len(self.numbers)
        # Максимальное число повторов каждой карты. Для счёта пары, сет, четверки
        self.maxu = max(self.nn) if len(self.nn) > 0 else 0

        # Отлов флеша
        if max(self.suits) >= 5:
            self.is_flush = True
            self.fs = Suit(self.suits.index(max(self.suits)))
            self.fd = [card for card in self.cards if card.suit == self.fs]

        if now_check:
            self.check(verbose=False)

    def __getitem__(self, i):
        return self.cards[i]

    def __eq__(self, other):
        if self._len == other._len and not len(self - other):
            return True

        return False

    def __len__(self):
        return self.cards.__len__()

    def __repr__(self):
        return self.cards.__repr__()

    def __str__(self):
        return self.cards.__repr__()

    def __add__(self, other):
        if other is not None:
            return Deck(self.cards + other.cards, now_check=False)
        else:
            return self

    def __sub__(self, other):
        if other is not None:
            temp = deepcopy(self.cards)

            for card in other.cards:
                if card in temp:
                    temp.remove(card)
                # else:
                #     raise PokerError(f'Can\'t substract. {card} not in deck {self}')

            return Deck(temp, now_check=False)

        else:
            return self

    def info(self):
        return self.is_flush, self.lenu, self.nn, self.suits

    def copy(self):
        return deepcopy(type(self)(self.cards))

    def remove(self, del_card):
        """
        Работает только при сортировки -- "карта без масти хуже карты с мастью". any_card_suit > 3
        Пример:
            2s > 2*
        """
        del_card = Card(del_card)
        if del_card in self.cards:
            for card in self.cards:
                if del_card == card:
                    self.cards.remove(card)
                    self.__init__(self.cards)
                    break

    def count(self, ref_card):
        return sum([1 if card == Card(ref_card) else 0 for card in self])

    def itercards(self):
        return zip(range(self._len), self.cards)

    def get_color(self):
        deck_color = [card.get_color() for card in self.cards]
        color = 'mix'
        if all([card == 'red' for card in deck_color]):
            color = 'red'
        elif all([card == 'black' for card in deck_color]):
            color = 'black'

        return color

    def check(self, verbose='points'):

        def highcard(cards):
            k = min(5, len(cards))
            wc = cards[:]
            wc.sort()
            wc = wc[-k:]
            points = sum([(wc[-j].get_number_int()) * (13**-j) for j in range(1, k + 1)])

            return wc, points

        # На стрит есть смысл проверять если уникальных карт больше-равно 5
        def straight(cards):
            for i in range(1, len(cards) + 1):
                high_card_int = cards[-i]
                current_card = cards[-i]
                straight_cards = [high_card_int]
                straight_len_count = 0

                # Берем старшую карты и идем от неё вниз, проверяя входит ли следующая в список карт
                while True:
                    if current_card - 1 in cards:
                        # straight_cards.append(current_card - 1)
                        # Добавляю в список конкретную карту из списка карт
                        straight_cards.append(cards[cards.index(current_card - 1)])
                        straight_len_count += 1
                        current_card -= 1

                        # Начали со старшей карты и добавили в стрит еще 4е карты -> пора выходить.
                        if straight_len_count == 4:
                            # Проверка что не пойдем по кругу, после тузов снова к королям
                            # Иначе найдет стрит '4d,3*,2*,A*,K*' тут '4c,2d,Ah,4d,3d,Qh,Kd'
                            if high_card_int.get_number_int() >= 3:
                                # Возвращает карту стрита и старшую карту стрита
                                straight_cards.sort()
                                return straight_cards, high_card_int.get_number_int()
                    else:
                        break

            return [], -1

        if self._len >= 5:
            wcards = [0] * 10
            wwcards = [0] * 10
            points = [0] * 10

            if not self.is_flush:
                if self.maxu == 1:
                    wcards[0], points[0] = highcard(self.cards)
                    wwcards[0] = wcards[0][-1:][:]

                elif self.maxu == 2:
                    if self.lenu == self._len-1:
                        wcards[1] = [self.cards[-i] for i
                                     in range(1, len(self.cards) + 1)
                                     if self.ncards[-i] == 2]
                        wwcards[1] = wcards[1][:]
                        i = self._len - 1
                        ac = []

                        while len(ac) < 3:
                            if not self.cards[i] in wcards[1]:
                                    ac.append(self.cards[i])
                            i -= 1

                        points[1] = 1 + float(wcards[1][-1].get_number_int()) / 13 + highcard(wcards[1] + ac)[1] / 169
                        wcards[1] += ac
                        wcards[1].sort()

                    elif self.lenu < self._len-1:  # check 3 pairs
                        wcards[2] = [self.cards[-i] for i in range(1, len(self.cards) + 1) if self.ncards[-i] == 2]
                        wcards[2] = wcards[2][:4]
                        wwcards[2] = wcards[2][:]
                        i = self._len - 1
                        ac = []

                        while len(ac) < 1:
                            if not self.cards[i] in wcards[2]:
                                ac.append(self.cards[i])
                            i -= 1

                        points[2] = 2 + wcards[2][-3].get_number_int() / 13 + wcards[2][-1].get_number_int() / 169 + highcard(wcards[2]+ac)[1] / 2197
                        wcards[2] += ac
                        wcards[2].sort()

                elif self.maxu == 3:
                    if self.lenu == self._len - 2:
                        wcards[3] = [self.cards[-i] for i in range(1, len(self.cards)+1) if self.ncards[-i] == 3]
                        wwcards[3] = wcards[3][:]
                        i = self._len - 1
                        ac = []

                        while len(ac) < 2:
                            if not self.cards[i] in wcards[3]:
                                ac.append(self.cards[i])
                            i -= 1

                        points[3] = 3 + wcards[3][-1].get_number_int() / 13 + highcard(wcards[3] + ac)[1] / 169
                        wcards[3] += ac
                        wcards[3].sort()

                    if self.lenu < self._len - 2:
                        part3 = [self.cards[-i] for i in range(1, len(self.cards) + 1) if self.ncards[-i] == 3]
                        part3.sort()

                        part2 = [self.cards[-i] for i in range(1, len(self.cards) + 1) if self.ncards[-i] == 2]
                        part2.sort()

                        wcards[6] = (part2 + part3)[-5:]
                        wwcards[6] = wcards[6][:]

                        # КОСТЫЛЬ :(
                        rk3 = wcards[6][-1].get_number_int()
                        rk2 = wcards[6][0].get_number_int()

                        points[6] = 6 + rk3 / 13 + rk2 / 169
                        wcards[6].sort()

                elif self.maxu == 4:
                        wcards[7] = [self.cards[-i] for i
                                     in range(1, len(self.cards) + 1)
                                     if self.ncards[-i] == 4]
                        wwcards[7] = wcards[7][:]
                        i = self._len - 1
                        ac = []

                        while len(ac) < 1:
                            if not self.cards[i] in wcards[7]:
                                    ac.append(self.cards[i])
                            i -= 1

                        points[7] = 7 + float(wcards[7][-1].get_number_int()) / 13 + highcard(wcards[7] + ac)[1] / 169
                        wcards[7] += ac
                        wcards[7].sort()

                if self.lenu >= 5:
                    straight_cards, high_card_int = straight(self.cards)

                    if high_card_int >= 0:
                        wcards[4] = straight_cards
                        wwcards[4] = wcards[4][:]
                        points[4] = 4 + high_card_int / 13

            elif self.is_flush:
                wcards[5], points[5] = highcard(self.fd)
                wwcards[5] = wcards[5][:]
                points[5] += 5

                if self.lenu >= 5:
                    straight_cards, high_card_int = straight(self.fd)

                    if high_card_int == 12:
                        wcards[9] = straight_cards
                        wwcards[9] = wcards[9][:]
                        points[9] = 9

                    elif high_card_int >= 0:
                        wcards[8] = straight_cards
                        wwcards[8] = wcards[8][:]
                        points[8] = 8 + high_card_int / 13


            self.points = max(points)
            self.wcards = wcards[points.index(self.points)]

        elif self._len == 2:
            self.points = 0
            self.wcards = self.cards

        if verbose and len(self.cards) >= 5:

            ranks = [i for i, combination in enumerate(wwcards) if isinstance(combination, list)]
            rank = max(ranks)

            if verbose == 'points':
                return self.points

            elif verbose == 'full':

                out = {'cards': self.cards,
                       'points': self.points,
                       'combination_name': comb_name_dict[rank],
                       'combination_cards': wwcards[rank],
                       'kicker': [card for card in self.wcards if card not in wwcards[rank]],
                       'top_five': self.wcards
                       }

                return out

            else:
                return self.points, self.wcards

        else:
            return {'cards': [],
                    'points': 0,
                    'combination_name': 'NotEnoughCard',
                    'combination_cards': [],
                    'kicker': [],
                    'top_five': []
                    }

class fulldeck:
    """
    creates full deck without excep_cards
    """
    def __init__(self, except_cards=[], shuffle=True):
        self.cards = [Card(nn) for nn in range(52) if Card(nn) not in except_cards]

        if shuffle:
            self.shuffle()

    def __len__(self):
        return self.cards.__len__()

    def __getitem__(self, i):
        return self.cards[i]

    def __sub__(self, cardlist, shuffle=True):
        if type(cardlist) == list or isinstance(cardlist, Deck):
            [self.cards.remove(card) for card in cardlist if card in self.cards]

        elif isinstance(cardlist, Card):
                self.cards.removed(cardlist)

        else:
            raise PokerError(f'Can\'t substract {cardlist}({type(cardlist)}) from deck')

        return self

    def __add__(self, cardlist, shuffle=True):
        if type(cardlist) == list or isinstance(cardlist, Deck):
            self.cards.extend([card for card in cardlist if card not in self.cards])

        elif isinstance(cardlist, Card):
            if card not in self.cards:
                self.cards.append(cardlist)

        else:
            raise PokerError(f'Can\'t add {cardlist}({type(cardlist)}) to deck')

        if shuffle:
            self.shuffle()

        return self

    def __repr__(self):
        return ','.join([str(item) for item in self.cards])

    def get_cards(self, cards_per_player=2, players_count=1, remove=True):
        result = []
        cards = self.cards[:players_count * cards_per_player]

        i = 0
        for k in range(players_count):
            deck = []
            for j in range(cards_per_player):
                deck.append(cards[i])
                i += 1

            result.append(Deck(deck, now_check=False))

        if remove:
            self = self - cards

        return result if players_count > 1 else result[0]

    def shuffle(self):
        random.shuffle(self.cards)


def _one_game(args):
    """
    hand -- Рука проверяемого игрока
    desk -- Карты на столе
    deck -- Колода (без карты на столе и в руке базового игрока)
    players_cnt -- количество игроков

    Возвращает 1 если базовый игрок выиграл и 0 если проиграл.
    """

    hand, desk, deck, players_cnt = args

    # Перемешать колоду для уникальности каждой раздачи
    random.shuffle(deck)

    full_desk = desk + [deck[i] for i in range(5 - len(desk))]
    hand_other = [deck[5 - len(desk) + i] for i in range((players_cnt - 1) * 2)]

    player_point = Deck(full_desk + hand).check()
    max_enemy_point = max([Deck(full_desk + hand_other[i * 2 : i * 2 + 2]).check() for i in range(players_cnt - 1)])

    if player_point >= max_enemy_point:
        return 1
    else:
        return 0

def monte_carlo(hand, desk, players_cnt, series, core):
    """
    series -- Количество симуляций
    core -- Чисто потоков расчета
    """

    if players_cnt > 1:

        hand = [Card(i) for i in hand.split(',')]
        desk = [Card(i) for i in desk.split(',')] if len(desk) > 0 else []
        deck = list(fulldeck(hand + desk))

        with Pool(core) as pool:
            win_ratio = sum(pool.map(_one_game, [(hand, desk, deck, players_cnt) for _ in range(series)]))

        return win_ratio / series

    else:
        return 1

if __name__ == '__main__':

    desk_cards = 'Ts,Js,Qs,2c,3d'
    players_hand = 'Ks,Ac'

    deck = Deck(','.join((desk_cards, players_hand)))
    print(deck.check())
    print(deck.check('full'))
