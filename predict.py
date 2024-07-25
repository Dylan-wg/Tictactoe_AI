import copy
import numpy as np

from Node import Node

from Chessboard import Chessboard
import nn
import random as rd

def main():
    order = rd.choice([1, -1])
    ju = order
    p_nn = nn.p_nn()
    p_nn.load_weights("p_nn.h5")
    v_nn = nn.v_nn()
    v_nn.load_weights("v_nn.h5")
    cb = Chessboard()
    q = True
    while q:
        if order == 1:
            cs = cb.get_coordinate()
            pres: list = p_nn.predict([cb.get_formatted_chessboard()])[0].tolist()

            #MCTS
            cbb = copy.deepcopy(cb)
            cbb.set_flag()
            root = Node(copy.deepcopy(cbb), cbb.get_flag(), coordinate=None)
            for _ in range(0, 10000):
                cbb = copy.deepcopy(cb)
                current = root
                while (not cbb.is_full()) and cbb.get_winner() == 0:
                    coor = rd.choice(cbb.get_coordinate())
                    cbb.drop(coor)
                    current = current.to_child(copy.deepcopy(cbb), cbb.get_flag(), coordinate=copy.deepcopy(coor))
                    current.increase()
                    cbb.judgement()
                    if cbb.get_winner() != 0 or cbb.is_full():
                        root.increase()
                        if cb.get_flag() == -1:
                            current.set_value(1 - (cbb.get_winner() / 2 + 0.5))
                        else: current.set_value(cbb.get_winner() / 2 + 0.5)
                        while not (current.get_parent() is None):
                            current = current.get_parent()
                            s = 0
                            for i in current.get_children():
                                s = s + i.get_value() * i.get_time()
                            p = s / current.get_time()
                            current.set_value(p)
                        current.get_parent()

            for i in root.get_children():
                adds = 30 ** (i.get_value() - 0.75) - 0.3
                '''print(pres)'''
                pres[i.get_coordinate()[0] * 3 + i.get_coordinate()[1]] += adds * 0.5
                '''print(i.get_coordinate())
                print(i.get_value())
                print(adds)
            print(pres)'''

            max_p = 0
            for i in cs:
                if max_p <= pres[i[0] * 3 + i[1]]:
                    max_p = pres[i[0] * 3 + i[1]]
                    pre_out = i

            cb.drop(pre_out)
            order *= (-1)
            print(pre_out)
            cb.show_chessboard()
            cb.judgement()
            if cb.get_winner() != 0 or cb.is_full():
                q = False
                continue
        elif order == -1:
            while True:
                ipt = input("Your turn:").split()
                for i in range(0, 2):
                    ipt[i] = int(ipt[i])
                if ipt in cb.get_coordinate():
                    break
            cb.drop(ipt)
            order *= (-1)
            cb.show_chessboard()
            cb.judgement()
            if cb.get_winner() != 0 or cb.is_full():
                q = False
                continue

    if ju == 1:
        if cb.get_winner() == 1:
            print("You lost.")
        elif cb.get_winner() == -1:
            print("You win.")
    elif ju == -1:
        if cb.get_winner() == -1:
            print("You lost.")
        elif cb.get_winner() == 1:
            print("You win.")


if __name__ == "__main__":
    main()
