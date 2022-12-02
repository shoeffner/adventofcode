from pathlib import Path

rock, paper, scissors = 1, 2, 3
loss, draw, win = 0, 3, 6

code1 = {
    'A X': rock + draw, 'A Y': paper + win,  'A Z': scissors + loss,
    'B X': rock + loss, 'B Y': paper + draw, 'B Z': scissors + win,
    'C X': rock + win,  'C Y': paper + loss, 'C Z': scissors + draw,
}

code2 = {
    'A X': scissors + loss, 'A Y': rock + draw,     'A Z': paper + win,
    'B X': rock + loss,     'B Y': paper + draw,    'B Z': scissors + win,
    'C X': paper + loss,    'C Y': scissors + draw, 'C Z': rock + win,
}

for strategy in (code1, code2):
    print(sum(strategy[round] for round in Path('input').read_text().splitlines()))
