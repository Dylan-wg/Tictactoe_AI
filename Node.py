class Node:

    def __init__(self, chessboard, flag, value=0, parent=None, coordinate=None):
        self.chessboard = chessboard
        self.coordinate = coordinate
        self.value = value
        self.parent = parent
        self.time = 0
        self.flag = flag
        self.children = []

    def get_parent(self):
        return self.parent

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def get_coordinate(self):
        return self.coordinate

    def get_chessboard(self):
        return self.chessboard

    def increase(self):
        self.time += 1

    def get_time(self):
        return self.time

    def to_child(self, chessboard, flag, value=0, coordinate=None):
        for i in self.children:
            if i.get_chessboard().get_formatted_chessboard() == chessboard.get_formatted_chessboard() and i.get_flag() == flag and i.get_coordinate() == coordinate:
                return i
        self.children.append(Node(chessboard, flag, value, parent=self, coordinate=coordinate))
        return self.children[-1]

    def get_children(self):
        return self.children

    def get_flag(self):
        return self.flag
