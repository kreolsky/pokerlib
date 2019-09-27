# pokerlib
Честно взято [[https://github.com/mrska1992/pokerlib|тут]] и немного дработано напильником

```python
from pokerlib import Deck

desk_cards = 'Ts,Js,Qs,2c,3d'
players_hand = 'Ks,As'

deck = Deck(','.join((desk_cards, players_hand)))
```
А потом вот так
```python
print(deck.info)
```
Ну или так
```python
print(deck['result_points'])
```

# Развлекайся, крч


