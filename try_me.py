from pokerlib import Deck

desk_cards = 'Ts,Js,Qs,2c,3d'
players_hand = 'Ks,Ac'

deck = Deck(','.join((desk_cards, players_hand)))
print(deck.check())
print(deck.check('full'))
