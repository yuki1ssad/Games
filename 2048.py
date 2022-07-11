import random
import msvcrt
import argparse
import os


class Display:
    def __init__(self, w, h, title, info = {}):
        self.board = [[ 0 for j in range(w) ] for i in range(h)]
        self.title = title
        self.info = info
    
    def __init__(self, board, title, info = {}):
        self.board = board
        self.title = title
        self.info = info
    
    def show(self, clear = True):
        if clear == True:
            os.system("cls") 
            
        print(f'{self.title}\n{self.info}')
        for row in self.board:
            for i in row:
                print('{:>4}'.format(i), end=' ')
            print('\n')

class Habdle_2048:
    def __init__(self, score):
        self.winscore = score
    
    def _align(self, lis, direction):
        z = lis.count(0)
        alist = [0 for i in range(z)]
        for i in range(z):
            lis.remove(0)
        if direction == 'left':
            lis.extend(alist)
        if direction == 'right':
            for i in range(z):
                lis.insert(0, 0)

    def _add_same(self, lis, direction):
        if direction == 'left':
            for i in range(len(lis) - 1):
                if lis[i] == lis[i + 1] and lis[i] != 0:
                    lis[i] *= 2
                    lis[i + 1] = 0
        elif direction == 'right':
            for i in range(len(lis) - 1, 0, -1):
                if lis[i] == lis[i - 1] and lis[i] != 0:
                    lis[i] *= 2
                    lis[i - 1] = 0
    
    def _operate(self, board, direction):       
        if direction == 'A' or direction == 'a':
            direction = 'left'
            for i in range(len(board)):
                self._align(board[i], direction)
                self._add_same(board[i], direction)
                self._align(board[i], direction)
    
        if direction == 'D' or direction == 'd':
            direction = 'right'
            for i in range(len(board)):
                self._align(board[i], direction)
                self._add_same(board[i], direction)
                self._align(board[i], direction)
        
        if direction == 'W' or direction == 'w':
            direction = 'left'
            
            height = len(board)
            width = len(board[0])
            board_t = [[board[j][i] for j in range(height)] for i in range(width)]
            
            for i in range(len(board_t)):
                self._align(board_t[i], direction)
                self._add_same(board_t[i], direction)
                self._align(board_t[i], direction)
            
            board = [[board_t[j][i] for j in range(width)] for i in range(height)]

        if direction == 'S' or direction == 's':
            direction = 'right'

            height = len(board)
            width = len(board[0])
            board_t = [[board[j][i] for j in range(height)] for i in range(width)]
            
            for i in range(len(board_t)):
                self._align(board_t[i], direction)
                self._add_same(board_t[i], direction)
                self._align(board_t[i], direction)
            
            board = [[board_t[j][i] for j in range(width)] for i in range(height)]
        
        return board
    
    def _count_zero(self, board):
        z_count = 0
        for i in range(len(board)):
            z_count += board[i].count(0)
        return z_count
    
    def _padnum(self, board):
        z_count = self._count_zero(board)
        k = random.randint(1, z_count)
        new_num = random.choice([2, 2, 4, 4, 4, 4, 8, 8, 8])
        
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 0:
                    k -= 1
                    if k == 0:
                        board[i][j] = new_num

    def _cannot_combine(self, board):
        flag = True
        for i in range(len(board)):
            for j in range(len(board[i]) - 1):
                if board[j] == board[j + 1]:
                    flag = False
                    return flag
        
        height = len(board)
        width = len(board[0])
        board_t = [[board[j][i] for j in range(height)] for i in range(width)]
        
        for i in range(len(board_t)):
            for j in range(len(board_t[i]) - 1):
                if board_t[j] == board_t[j + 1]:
                    flag = False
                    return flag
        return flag
    
    def _presantScore(self, board):
        maxScore = 0
        for row in board:
            if maxScore < max(row):
                maxScore = max(row)
        return maxScore
    
    def over_check(self, board, direction):
        board = self._operate(board, direction)
        presant_score = self._presantScore(board)
        
        if presant_score >= self.winscore:
            return ['WIN', board]
        elif self._count_zero(board) == 0 and self._cannot_combine(board):
            return ['FAIL', board]
        else:
            self._padnum(board)
            return ['CONTINUE', board]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', help='board width', type=int)
    parser.add_argument('--height', help='board height', type=int)
    args = parser.parse_args()

    displayer = Display(board=[[random.choice([0, 0, 0, 2, 2, 4]) for x in range(args.width)]
                               for i in range(args.height)],
                        title='__2048__',
                        info={'ROUND': 0, 'SCORE': 0})
    
    handle = Habdle_2048(score=2048)
    
    state = 'CONTINUE'
    
    while(state == 'CONTINUE'):
        displayer.show()
        print("please input an order: [W/w(up) S/s(down) A/a(left) D/d(right)] ")
        dir = msvcrt.getch().decode('ASCII')
        
        if dir == 'Q' or dir == 'q':
            exit()
        
        res = handle.over_check(board=displayer.board, direction=dir)
        state = res[0]
        displayer.board = res[1]
    else:
        if state == 'WIN':
            print('YOU WIN')
            exit()
        elif state == 'FAIL':
            print('YOU FAIL')
            exit()
        
        
        