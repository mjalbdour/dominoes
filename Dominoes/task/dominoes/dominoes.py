
from random import choice, choices

MSG_HEADER = "=" * 70
MSG_STOCK_SIZE = "Stock size:"
MSG_COMPUTER_PIECES = "Computer pieces:"
MSG_YOUR_PIECES = "Your pieces:"
MSG_STOCK = "Stock pieces:"
MSG_COMPUTER = "Computer pieces:"
MSG_PLAYER = "Player pieces:"
MSG_DOMINO_SNAKE = "Domino snake:"
MSG_STATUS = "Status:"
MSG_STATUS_COMPUTER = "Computer is about to make a move. Press Enter to continue..."
MSG_STATUS_PLAYER = "It's your turn to make a move. Enter your command."


def create_dominoes():
    _dominoes = []
    for i in range(7):
        for j in range(i, 7):
            _dominoes.append([i, j])
    return _dominoes


def reshuffle():
    _stock = choices(dominoes, k=14)
    dom_stock_exclusive = [x for x in dominoes if x not in _stock]
    _computer = []
    while len(_computer) < 7:
        domino = choice(dom_stock_exclusive)
        if domino not in _computer:
            _computer.append(domino)

    dom_stock_comp_exclusive = [x for x in dom_stock_exclusive if x not in _computer]
    _player = []
    while len(_player) < 7:
        domino = choice(dom_stock_comp_exclusive)
        if domino not in _player:
            _player.append(domino)

    return _stock, _computer, _player


def check_doubles():
    _max_double_computer = [-1, -1]
    for i in range(6, -1, -1):
        if [i, i] in computer and i > _max_double_computer[0]:
            _max_double_computer = [i, i]
            break

    _max_double_player = [-1, -1]
    for i in range(6, -1, -1):
        if [i, i] in player and i > _max_double_player[0]:
            _max_double_player = [i, i]
            break

    return _max_double_computer != [-1, -1] and _max_double_player != [-1, -1], _max_double_computer, _max_double_player


def print_player_pieces(player_pieces):
    print(f'\n{MSG_YOUR_PIECES}')
    for i, piece in enumerate(player_pieces):
        print(f'{i+1}:{piece}')


dominoes = create_dominoes()
stock, computer, player = reshuffle()
result = check_doubles()
while not result[0]:
    stock, computer, player = reshuffle()
    result = check_doubles()


domino_snake = None
status = ""
if result[1] != [-1, -1] and result[1] != [-1, -1]:
    if result[1] > result[2]:
        domino_snake = result[1]
        computer.remove(result[1])
        status = "player"
    else:
        domino_snake = result[2]
        player.remove(result[2])
        status = "computer"


print(f'{MSG_HEADER}')
print(f'{MSG_STOCK_SIZE} {len(stock)}')
print(f'{MSG_COMPUTER_PIECES} {len(computer)}')
print(f'\n{domino_snake}')
print_player_pieces(player)

if status == "player":
    print(f'\n{MSG_STATUS} {MSG_STATUS_PLAYER}')
elif status == "computer":
    print(f'\n{MSG_STATUS} {MSG_STATUS_COMPUTER}')
