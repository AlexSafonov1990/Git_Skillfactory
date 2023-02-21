import random

SIZE = 6
# Измените значение константы RADAR, если хотите отрисовать поле противника
RADAR = True

_s_buffer = "•"
_s_ship = "■"
_s_space = "."
_s_hit = "+"
_s_destroyed = "X"
_s_miss = "*"

SHIPS_LIST = [[1, 3], [2, 2], [4, 1]]


class Board(object):

    def __init__(self):
        self.board = []
        self.spawned = []

    def create(self):
        for row in range(SIZE):
            self.board.append([_s_space] * SIZE)

    def randomize(self):
        for ship in SHIPS_LIST:
            for unit in range(ship[0]):

                spawning = True
                while spawning:

                    global refer
                    refer = random.randrange(2)
                    if refer == 0:
                        location_y = random.randrange(SIZE)
                        location_x = random.randrange(SIZE - (ship[1] - 1))
                    else:
                        location_y = random.randrange(SIZE - (ship[1] - 1))
                        location_x = random.randrange(SIZE)

                    offset = 0
                    for testing in range(ship[1]):
                        if refer == 0 and self.board[location_y][location_x + offset] != _s_space:
                            break
                        elif refer == 1 and self.board[location_y + offset][location_x] != _s_space:
                            break
                        offset += 1
                        if offset == ship[1]:
                            spawning = False

                offset = 0
                current_ship = []
                for marker in range(ship[1]):
                    if refer == 0:
                        self.board[location_y][location_x + offset] = _s_ship
                        current_ship.append([location_y, location_x + offset])
                    else:
                        self.board[location_y + offset][location_x] = _s_ship
                        current_ship.append([location_y + offset, location_x])
                    offset += 1
                self.spawned.append(current_ship)

                for unit_point in current_ship:
                    for buffer_point in ([0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]):
                        b_point_y = unit_point[0] + buffer_point[0]
                        b_point_x = unit_point[1] + buffer_point[1]
                        if b_point_y in range(SIZE) and b_point_x in range(SIZE):
                            if self.board[b_point_y][b_point_x] == _s_space:
                                self.board[b_point_y][b_point_x] = _s_buffer

    def updating(self, ship):
        for unit in ship:
            for buffer_point in ([0, 0], [0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]):
                b_point_y = unit[0] + buffer_point[0]
                b_point_x = unit[1] + buffer_point[1]
                if b_point_y in range(SIZE) and b_point_x in range(SIZE):
                    if self.board[b_point_y][b_point_x] == _s_buffer:
                        self.board[b_point_y][b_point_x] = _s_miss
                    elif self.board[b_point_y][b_point_x] == _s_hit:
                        self.board[b_point_y][b_point_x] = _s_destroyed


def print_boards():
    print("\n    Ваше поле" + (" " * (SIZE - 1)) + "Поле противника")
    print("    " + (" ".join(str(i) for i in list(range(SIZE)))), end=(" " * 3))
    print("    " + (" ".join(str(i) for i in list(range(SIZE)))))
    print("   " + (" |" * SIZE), end=(" " * 3))
    print("   " + (" |" * SIZE))
    n = 0
    for i in range(SIZE):
        if RADAR:
            print(str(n) + " - " + " ".join(str(i) for i in player.board[n]), end=(" " * 3))
            print(str(n) + " - " + " ".join(str(i) for i in ai.board[n]))
        else:
            print(str(n) + " - " + " ".join(str(i) for i in player.board[n]).replace(_s_buffer, _s_space),
                  end=(" " * 3))
            print(str(n) + " - " + " ".join(str(i) for i in ai.board[n]).replace(_s_ship, _s_space).replace(_s_buffer,
                                                                                                            _s_space))
        n += 1


def press_ent():
    input("Нажмите 'ENTER', чтобы продолжить.\n")


def state_of_ships(enemy):
    global destroy
    destroy = True
    for d_ship in enemy.spawned:
        damage = 0
        for d_unit in d_ship:
            if enemy.board[d_unit[0]][d_unit[1]] == _s_hit:
                damage += 1
        if damage == len(d_ship):
            enemy.updating(d_ship)
            enemy.spawned.remove(d_ship)
            destroy = False


def ai_pass():
    ai_guessing = True
    while ai_guessing:

        ai_intuition = random.randrange(SIZE * 5)

        if ai_intuition == 0:
            ai_int_ship = random.randrange(len(player.spawned))
            ai_int_unit = random.randrange(len(player.spawned[ai_int_ship]))
            ai_guess_y = player.spawned[ai_int_ship][ai_int_unit][0]
            ai_guess_x = player.spawned[ai_int_ship][ai_int_unit][1]

        else:
            ai_guess_y = random.randrange(SIZE)
            ai_guess_x = random.randrange(SIZE)

        if player.board[ai_guess_y][ai_guess_x] == _s_ship:
            player.board[ai_guess_y][ai_guess_x] = _s_hit
            state_of_ships(player)
            if destroy:
                print("\nПротивник уничтожил ваше судно (X: %s, Y: %s)." % (ai_guess_x, ai_guess_y))
            else:
                print("\nПротивник повредил ваше судно (X: %s, Y: %s)." % (ai_guess_x, ai_guess_y))
            break

        elif player.board[ai_guess_y][ai_guess_x] == _s_space or player.board[ai_guess_y][ai_guess_x] == _s_buffer:
            player.board[ai_guess_y][ai_guess_x] = _s_miss
            print("\nПротивник выстрелил мимо (X: %s, Y: %s)." % (ai_guess_x, ai_guess_y))
            print_boards()
            break

        else:
            continue


ai = Board()
ai.create()
ai.randomize()


def player_pass():
    while True:
        try:
            x = int(input("Введите номер строки (от 0 до {}): ".format(SIZE - 1)))
            y = int(input("Введите номер столбца (от 0 до {}): ".format(SIZE - 1)))
            if x not in range(SIZE) or y not in range(SIZE):
                print("Неверные координаты, попробуйте снова.")
                continue
            elif ai.board[x][y] in [_s_miss, _s_hit, _s_destroyed]:
                print("Вы уже стреляли в эту клетку, попробуйте снова.")
                continue
            break
        except ValueError:
            print("Неверный ввод, попробуйте снова.")

    if ai.board[x][y] == _s_buffer:
        print("\nВы промахнулись!")
        ai.board[x][y] = _s_miss
    elif ai.board[x][y] == _s_ship:
        print("\nВы попали!")
        ai.board[x][y] = _s_hit
        state_of_ships(ai)
    elif destroy:
        print("\nВы уничтожили судно противника")

def main():
    global player, ai
    player = Board()
    ai = Board()
    print("Добро пожаловать в игру 'Морской Бой!'")
    print("У вас на поле океана располагаются корабли.")
    print("Ваша задача - найти их и уничтожить.")
    print("Помните, что игра идет против компьютера.\n")

    player.create()
    ai.create()

    player.randomize()
    ai.randomize()

    print_boards()

    while True:
        player_pass()
        state_of_ships(ai)
        if not ai.spawned:
            print("Поздравляем, вы выиграли!")
            break

        ai_pass()
        state_of_ships(player)
        if not player.spawned:
            print("К сожалению, вы проиграли.")
            break


main()
