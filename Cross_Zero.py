game_board = list(range(1, 10))
comb_to_win = [
    (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 2, 3),
    (4, 5, 6), (7, 8, 9), (1, 5, 9), (3, 5, 7)
]
corr_dig = '123456789'


def get_board():
    print('---------')
    for each in range(3):
        print(game_board[0 + each * 3], '|',
              game_board[1 + each * 3], '|',
              game_board[2 + each * 3])
    print('---------')


def get_sign(sign):
    while True:
        cross_zero = int(input(f'Куда поставить: {sign} ? '))
        if not (str(cross_zero) in corr_dig):
            print('Ошибка. Повторите ввод')
            continue
        if str(game_board[cross_zero - 1]) in 'XO':
            print('Клетка занята')
            continue
        game_board[cross_zero - 1] = sign
        break


def check_to_win():
    for each in comb_to_win:
        if (game_board[each[0] - 1]) == (game_board[each[1] - 1]) == (game_board[each[2] - 1]):
            return 'Кто выиграл?'

    else:
        return False


def main():
    counter = 0
    while True:
        get_board()
        if counter % 2 == 0:
            get_sign('X')
        else:
            get_sign('O')
        if counter > 3:
            winner = check_to_win()
            if winner:
                get_board()
                print(winner, 'выиграл!')
                break
        counter += 1
        if counter > 8:
            get_board()
            print('Ничья!')
            break


if __name__ == '__main__':
    main()
