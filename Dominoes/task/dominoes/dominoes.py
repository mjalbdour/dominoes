# TODO: REFACTOR ABSOLUTE GARBAGE IN APPLY_MOVE FUNC XD
from random import choice, sample

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
MSG_STATUS_GAME_OVER = "The game is over."
MSG_STATUS_WON_PLAYER = "You won!"
MSG_STATUS_WON_COMPUTER = "The computer won!"
MSG_STATUS_DRAW = "It's a draw!"
MSG_ERROR_INVALID_INPUT = "Invalid input. Please try again."
MSG_ILLEGAL_MOVE = "Illegal move. Please try again."


def create_dominoes():
    _dominoes = []
    for i in range(7):
        for j in range(i, 7):
            _dominoes.append([i, j])
    return _dominoes


def reshuffle():
    _stock = sample(dominoes, k=14)
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


def validate_move_range(_move):
    return -len(player) <= _move <= len(player)


def input_move_player():
    while True:
        _move = input()
        try:
            _move = int(_move)
            if validate_move_range(_move):
                if apply_move(_move, "player"):
                    break
                else:
                    print(MSG_ILLEGAL_MOVE)
            else:
                print(MSG_ERROR_INVALID_INPUT)
        except ValueError:
            print(MSG_ERROR_INVALID_INPUT)


def generate_ai_moves():
    piece_side_count = dict.fromkeys([i for i in range(7)], 0)
    piece_score = dict.fromkeys([tuple(i) for i in computer], 0)
    for piece in domino_snake:
        piece_side_count[piece[0]] += 1
        piece_side_count[piece[1]] += 1

    for piece in computer:
        piece_side_count[piece[0]] += 1
        piece_side_count[piece[1]] += 1

    for piece in computer:
        piece_score[tuple(piece)] = piece_side_count[piece[0]] + piece_side_count[piece[1]]
    return [list(k) for k, v in sorted(piece_score.items(), key=lambda item: item[1], reverse=True)]


def apply_move_computer(piece):
    piece_index = computer.index(piece)
    if apply_move(piece_index, "computer") or apply_move(- piece_index, "computer"):
        return True
    else:
        return False


def input_move_computer():
    _ = input()
    _moves = generate_ai_moves()
    for move in _moves:
        if apply_move_computer(move):
            return

    apply_move(0, "computer")


def apply_move(_move, _status):
    if _move == 0:
        if stock:
            piece = choice(stock)
            status_corresponding_player[_status].append(piece)
            stock.remove(piece)
        return True
    else:
        piece = status_corresponding_player[_status][abs(_move) - 1]
        if _move > 0:
            if piece[0] == domino_snake[-1][1]:
                domino_snake.append(piece)
                status_corresponding_player[_status].remove(piece)
                return True
            elif piece[1] == domino_snake[-1][1]:
                domino_snake.append(piece[::-1])
                status_corresponding_player[_status].remove(piece)
                return True
        elif _move < 0:
            if piece[1] == domino_snake[0][0]:
                domino_snake.insert(0, piece)
                status_corresponding_player[_status].remove(piece)
                return True
            elif piece[0] == domino_snake[0][0]:
                domino_snake.insert(0, piece[::-1])
                status_corresponding_player[_status].remove(piece)
                return True

    return False


def check_ends_and_8times():
    num = domino_snake[0][0]
    count = 0
    if num == domino_snake[-1][1]:
        count += 2
        for piece in domino_snake[1:-1]:
            if num in piece:
                count += 1

    return count == 8


def check_draw():
    return check_ends_and_8times()


def switch_status(_status):
    if _status == "player":
        return "computer"

    return "player"


def print_player_pieces(player_pieces):
    print(f'{MSG_YOUR_PIECES}')
    for i, piece in enumerate(player_pieces):
        print(f'{i+1}:{piece}')


def print_domino_snake(snake):
    if len(snake) < 6:
        for i in range(0, len(snake)):
            if i == len(snake) - 1:
                print(snake[i])
            else:
                print(snake[i], end='')

    else:
        for i in range(0, 3):
            print(snake[i], end='')

        print("...", end='')

        for i in range(3, 0, -1):
            if i == 1:
                print(snake[-i])
            else:
                print(snake[-i], end='')


dominoes = create_dominoes()
stock, computer, player = reshuffle()
result = check_doubles()
while not result[0]:
    stock, computer, player = reshuffle()
    result = check_doubles()


domino_snake = []
status = ""
if result[1] != [-1, -1] and result[2] != [-1, -1]:
    if result[1] > result[2]:
        domino_snake.append(result[1])
        computer.remove(result[1])
        status = "player"
    else:
        domino_snake.append(result[2])
        player.remove(result[2])
        status = "computer"


status_corresponding_player = {
    "player": player,
    "computer": computer
}

while True:
    print(f'{MSG_HEADER}')
    print(f'{MSG_STOCK_SIZE} {len(stock)}')
    print(f'{MSG_COMPUTER_PIECES} {len(computer)}')
    print_domino_snake(domino_snake)
    print_player_pieces(player)

    if not player:
        print(f'{MSG_STATUS} {MSG_STATUS_GAME_OVER} {MSG_STATUS_WON_PLAYER}')
        break
    elif not computer:
        print(f'{MSG_STATUS} {MSG_STATUS_GAME_OVER} {MSG_STATUS_WON_COMPUTER}')
        break
    elif check_draw() or not stock:
        print(f'{MSG_STATUS} {MSG_STATUS_GAME_OVER} {MSG_STATUS_DRAW}')
        break

    if status == "player":
        print(f'\n{MSG_STATUS} {MSG_STATUS_PLAYER}')
        input_move_player()

    elif status == "computer":
        print(f'\n{MSG_STATUS} {MSG_STATUS_COMPUTER}')
        input_move_computer()

    status = switch_status(status)
