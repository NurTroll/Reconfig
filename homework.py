game_field = [['стол', 'стул1', 'шкаф'], ['стул', ' ', 'кресло']]
number_of_moves = 0
while game_field[0][2] != 'кресло' or game_field[1][2] != 'шкаф':
    print(*game_field, sep='\n')
    print('----------------------------')
    element = input("Введите предмет которы собираетесь передвинуть: ")
    number_of_moves += 1
    row2, row1, col2, col1 = 0, 0, 0, 0
    for i in range(len(game_field)):
        for j in range(len(game_field[i])):
            if game_field[i][j] == element:
                col1, row1 = i, j
            elif game_field[i][j] == ' ':
                col2, row2 = i, j

    if (row1 == row2 and abs(col1 - col2) == 1) or (col1 == col2 and abs(row1 - row2) == 1):
        game_field[col1][row1], game_field[col2][row2] = game_field[col2][row2], game_field[col1][row1]
        print(col1, row1)
        print(col2, row2)
    else:
        print("Неправильный ход!")

print(f'Поздравляю вы выиграли! У вас на это ушло {number_of_moves} ходов')