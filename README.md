# pokerlib
Честно взято [тут](https://github.com/mrska1992/pokerlib) исправлена какая-то бага и немного дработано напильником для совместимости с 3 питоном.

```python
from pokerlib import Deck

desk_cards = 'Ts,Js,Qs,2c,3d'
players_hand = 'Ks,As'

deck = Deck(','.join((desk_cards, players_hand)))
```
А потом вот так
```python
print(deck.check())
```
Ну или так
```python
print(deck.check('full'))
```

# Развлекайся, крч


