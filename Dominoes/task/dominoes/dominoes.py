
from random import choice, choices

MSG_STOCK = "Stock pieces:"
MSG_COMPUTER = "Computer pieces:"
MSG_PLAYER = "Player pieces:"
MSG_DOMINO_SNAKE = "Domino snake:"
MSG_STATUS = "Status:"

dominoes = []
for i in range(7):
    for j in range(i, 7):
        dominoes.append([i, j])


def reshuffle():
    _stock = choices(dominoes, k=14)

    _computer = []
    while len(_computer) < 7:
        domino = choice(dominoes)
        if domino not in _stock:
            _computer.append(domino)

    _player = []
    while len(_player) < 7:
        domino = choice(dominoes)
        if domino not in [_stock, _computer]:
            _player.append(domino)

    return _stock, _computer, _player


def check_doubles():
    _max_double_computer = [-1, -1]
    for _i in range(6, -1, -1):
        if [_i, _i] in computer and _i > _max_double_computer[0]:
            _max_double_computer = [_i, _i]
            break

    _max_double_player = [-1, -1]
    for _i in range(6, -1, -1):
        if [_i, _i] in player and _i > _max_double_player[0]:
            _max_double_player = [_i, _i]
            break

    return _max_double_computer != [-1, -1] and _max_double_player != [-1, -1], _max_double_computer, _max_double_player


stock, computer, player = reshuffle()
result = check_doubles()
while not result[0]:
    stock, computer, player = reshuffle()
    result = check_doubles()


domino_snake = []
status = ""
if result[1] != [-1, -1] and result[1] != [-1, -1]:
    if result[1] > result[2]:
        domino_snake.append(result[1])
        computer.remove(result[1])
        status = "player"
    else:
        domino_snake.append(result[2])
        player.remove(result[2])
        status = "computer"


print(f'{MSG_STOCK} {stock}')
print(f'{MSG_COMPUTER} {computer}')
print(f'{MSG_PLAYER} {player}')
print(f'{MSG_DOMINO_SNAKE} {domino_snake}')
print(f'{MSG_STATUS} {status}')
