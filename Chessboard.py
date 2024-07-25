class Chessboard:

    def __init__(self):
        self.chessboard = [[0, 0, 0] for i in range(0, 3)]
        self.flag = 1
        self.winner = 0
    def drop(self, coordinate):
        self.chessboard[coordinate[0]][coordinate[1]] = self.flag
        self.flag = self.flag*(-1)

    def show_chessboard(self):
        print(self.chessboard)

    def get_chessboard(self):
        return self.chessboard

    def get_formatted_chessboard(self):
        rt = []
        for i in range(0,3):
            for j in range(0,3):
                rt.append(self.chessboard[i][j])
        return rt

    def judgement(self):
        for i in range(0, 3):
            self.winner = int((self.chessboard[i][0]+self.chessboard[i][1]+self.chessboard[i][2])/3)
            if self.winner != 0:
                return

        self.winner = int((self.chessboard[0][0]+self.chessboard[1][1]+self.chessboard[2][2])/3)
        if self.winner != 0:
            return

        self.winner = int((self.chessboard[0][2]+self.chessboard[1][1]+self.chessboard[2][0])/3)
        if self.winner != 0:
            return

        for i in range(0, 3):
            self.winner = int((self.chessboard[0][i]+self.chessboard[1][i]+self.chessboard[2][i])/3)
            if self.winner != 0:
                return

    def get_winner(self):
        return self.winner

    def clear(self):
        self.__init__()
        self.flag = 1

    def is_full(self):
        for i in range(0,3):
            for j in range(0,3):
                if self.chessboard[i][j] == 0:
                    return False
        return True

    def get_coordinate(self):
        rt = []
        for i in range(0, 3):
            for j in range(0, 3):
                if self.chessboard[i][j] == 0:
                    rt.append([i, j])
        return rt

    def get_flag(self):
        return self.flag

    def set_flag(self):
        n = 0
        p = 0
        for i in range(0, 3):
            for j in range(0, 3):
                if self.chessboard[i][j] == 1:
                    p += 1
                elif self.chessboard[i][j] == -1:
                    n += 1
        if n == p:
            self.flag = 1
        else:
            self.flag = -1

if __name__ == "__main__":
    chessboard = Chessboard()

    chessboard.drop([0, 0])
    chessboard.drop([1, 1])
    chessboard.drop([0, 2])
    chessboard.drop([2, 2])
    chessboard.drop([0, 1])
    chessboard.show_chessboard()
    chessboard.judgement()
    print(chessboard.get_winner())
