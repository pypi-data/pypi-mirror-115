"""
https://en.wikipedia.org/wiki/List_of_poker_hands

task: 
Implement the `special_type` function to cover the cases marked with an asterisk.

  | Type            | # | Example           | Type tuple      |
  |-----------------|---|-------------------|-----------------|
  | Five of a kind  | 9 | As Ac Ah Ad Aj    | (5,)            |
* | Straight flush  | 8 | As Ks Qs Ts Js    | (4, 2)          |
  | Four of a kind  | 7 | 7s 7c 7d 2d 7h    | (4, 1)          |
  | Full house      | 6 | 8h 9c 8d 8c 9h    | (3, 2)          |
* | Flush           | 5 | 8c Kc Qc Jc Tc    | (3, 1, 3)       |
* | Straight        | 4 | Kc Qh Jd Th 9c    | (3, 1, 2)       |
  | Three of a kind | 3 | Ts Tc Th 9s 7c    | (3, 1, 1)       |
  | Two pair        | 2 | Ts Tc 9s 9c 7h    | (2, 2, 1)       |
  | One pair        | 1 | 3s 3c As Ks Qs    | (2, 1, 1, 1)    |
  | High card       | 0 | 2s 4s 5s 6s 7h    | (1, 1, 1, 1, 1) |

"""

from collections import Counter
from itertools import permutations
from copy import copy
# Data Types
Card = str  # A card is a str of length 2: '7s'
Hand = (list, tuple)  # A hand is 5 cards in either a list or a tuple

# Functions and Objects
join = ' '.join  # Function to join cards together into one string
cards = str.split  # Function to split a string apart into a list of cards
rankstr = '23456789TJQKA'  # Card ranks in ascending order


def rank(card) -> int:
    return rankstr.index(card[0]) + 2


def suit(card) -> str:
    return card[1]


def ranking(hand) -> tuple:
    """Return a value indicating how high the hand ranks."""
    counts = Counter(map(rank, hand))
    groups = sorted(((counts[r], r) for r in counts), reverse=True)
    type_, ranks = zip(*groups)
    if ranks == (14, 5, 4, 3, 2):
        ranks = (5, 4, 3, 2, 1)
    type_ = special_type(hand, ranks) or type_
    return type_, ranks


def the_same(things) -> bool:
    """Are all the things actually the same?"""
    return len(set(things)) <= 1


def special_type(hand, ranks) -> tuple:
    """For a flush or straight, return a tuple comparable with `type` in `ranking`."""
    _type = None
    if len(set(ranks)) == 1:
        return _type
    straight = False
    flash = len(set([card[1] for card in hand])) == 1
    if len(ranks) == 5:
        for num, i in enumerate(ranks):
            if num != len(ranks) - 1:
                if abs(i-ranks[num+1]) == 1:
                    continue
                else:
                    break
        else:
            straight = True
    if flash:
        _type = (3, 1, 3) if not straight else (4, 2)
    elif straight:
        _type = (3, 1, 2)
    return _type


hands = [cards(h) for h in (
    'As Ac Ah Ad Ad', 'Kh Kd Ks Kc Kh', '3h 3s 3d 3c 3c', '2s 2c 2d 2h 2h',  # 5 of a kind
    'As Ks Qs Ts Js', 'Kc Qc Jc Tc 9c', '6d 5d 4d 3d 2d', '5h 4h 3h 2h Ah',  # straight flush
    'As Ac Ad Ah 2s', '7s 7c 7d 2d 7h', '6s 6c 6d 6h 9s', 'As 5h 5c 5d 5s',  # four of a kind
    'Th Tc Td 5h 5c', '9h 9c 9d 8c 8h', '6h 6c 6d Tc Th', '5c 5d 5s As Ah',  # full house
    'As 2s 3s 4s 6s', 'Kc Qc Jc Tc 2c', 'Qc Jc Tc 9c 7c', '4h 5h 6h 7h 9h',  # flush
    'As Kd Qc Td Jh', 'Kc Qh Jd Th 9c', '6c 5d 4h 3s 2s', 'As 2d 3c 4h 5s',  # straight
    'As Ac Ad 2h 3h', 'Ts Tc Th 9s 8c', 'Ts Tc Th 9s 7c', '9h 9s 9d Ah Kh',  # three of a kind
    'Ts Tc 5s 5c 8h', 'Ts Tc 5s 5c 7h', '9s 9c 8s 8c As', '3s 3c 2s 2d Ah',  # two pair
    'As Ac 4c 5s 6s', '4s 4c As Ks Qs', '4h 4d Kh Qd Jd', '2d 2c Ad Kd Qd',  # pair
    'Ah 3s 4s 5s 6s', 'Kh Qh Jh Th 8d', '7d 2s 4s 5s 6s', '7h 6s 5d 3s 2d',  # high card
)]


def test(ranking, hands=None) -> bool:
    """Test that `ranking` preserves order of `hands`, and that permuting cards is irrelevant."""
    if hands is None:
        hands = []
    assert hands == sorted(hands, key=ranking, reverse=True)
    trans = str.maketrans('shdc', 'hscd')
    for hand in hands:
        assert the_same(ranking(h) for h in permutations(hand))
        assert the_same([ranking(hand), ranking([c.translate(trans) for c in hand])])
    return len(hands) > 0

print(test(ranking, hands))
