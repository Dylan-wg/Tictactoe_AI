import nn
from Node import Node
from Chessboard import Chessboard
import random as rd
import copy
import pickle


def uct(q, p, n, c):
    rt = q + 1.4 * p * ((n ** 0.5) / (1 + c))
    return rt

def check(d: list):
    n = 0
    p = 0
    for i in d:
        if i == 1:
            p+=1
        if i == -1:
            n+=1
    if p == n:
        return 1
    else:
        return -1

def main():
    v_nn = nn.v_nn()
    p_nn = nn.p_nn()
    cb = Chessboard()
    root = Node(None, None)

    for _ in range(0, 2):

        try:
            v_nn.load_weights("v_nn.h5")
            p_nn.load_weights("p_nn.h5")
        except FileNotFoundError:
            pass

        v_data = []
        v_labels = []

        for _ in range(0, 200):
            cb.clear()
            current = root
            while not cb.is_full():
                q = v_nn.predict([cb.get_formatted_chessboard()])[0].tolist()[0]
                ps = p_nn.predict([cb.get_formatted_chessboard()])[0].tolist()
                cs = cb.get_coordinate()
                ucts = {}
                ch = current.get_children()
                for i in cs:
                    u = 0
                    p = rd.randint(0, 8)
                    c = 0
                    for j in ch:
                        if i == j:
                            c = j.get_time()
                            p = ps[i[0]+i[1]*3]
                        else: c = 0
                    n = current.get_time()
                    u = uct(q=q, p=p, c=c, n=n)
                    ucts[str(i)] = u
                maximum = max(ucts.values())
                keys = [key for key, value in ucts.items() if value == maximum]
                coor = rd.choice(keys)
                print(coor)
                print(ucts)
                coor = [int(coor[1]), int(coor[4])]


                cb.drop(coor)
                current = current.to_child(copy.deepcopy(cb), cb.get_flag(), coordinate=copy.deepcopy(coor))
                current.increase()
                cb.judgement()
                if cb.get_winner() != 0 or cb.is_full():
                    root.increase()
                    current.set_value(cb.get_winner() / 2 + 0.5)
                    v_data.append(current.get_chessboard().get_formatted_chessboard())
                    v_labels.append(current.get_value())

                    while not (current.get_parent().get_parent() is None):
                        current = current.get_parent()
                        s = 0
                        for i in current.get_children():
                            s = s + i.get_value() * i.get_time()
                        p = s / current.get_time()
                        current.set_value(p)
                        v_data.append(current.get_chessboard().get_formatted_chessboard())
                        v_labels.append(current.get_value())
                    current.get_parent()
                    break

        print(v_data)
        print(v_labels)

        v_nn.fit(x=v_data, y=v_labels, epochs=1000, batch_size=500)
        v_nn.save_weights("v_nn.h5")

        p_data = v_data
        p_labels = []
        for d in p_data:
            labels = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            d_copy = copy.deepcopy(d)
            for i in range(0, 9):
                if d_copy[i] == 0:
                    d_copy[i] = check(d_copy)
                    out = v_nn.predict([d_copy])[0].tolist()[0]
                    if check(d_copy) == 1:
                        out = 1-out
                    labels[i] = out
                    d_copy[i] = 0
            s = 0
            for i in range(0, 9):
                s += labels[i]
            for i in range(0, 9):
                try:
                    labels[i] = labels[i] / s
                except ZeroDivisionError:
                    pass
            p_labels.append(labels)

        print(p_data)
        print(p_labels)

        p_nn.fit(x=p_data, y=p_labels, epochs=1000, batch_size=500)
        p_nn.save_weights("p_nn.h5")



if __name__ == "__main__":
    main()
