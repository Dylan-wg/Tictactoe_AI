import pygame
import sys
import random as rd
import nn
from Chessboard import Chessboard
import tkinter as tk
import copy
from Node import Node

def area_judgement(mx, my):
    x, y = 0, 0
    if 5 <= mx <= 195:
        x = 0
    elif 205 <= mx <= 395:
        x = 1
    elif 405 <= mx <= 595:
        x = 2
    if 5 <= my <= 195:
        y = 0
    elif 205 <= my <= 395:
        y = 1
    elif 405 <= my <= 595:
        y = 2
    return [x, y]

def main():

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    p_nn = nn.p_nn()
    cb = Chessboard()
    order = rd.choice([1, -1])

    '''Initialization'''
    pygame.init()
    screen = pygame.display.set_mode(size=[600, 600])
    pygame.display.set_caption("Tictactoe")
    h_pos = []
    c_pos = []

    '''Functions'''
    def draw_circle(x, y):
        pygame.draw.circle(screen, BLACK, (x, y), 80, 10)

    def draw_cross(x, y):
        pygame.draw.line(screen, BLACK, (x - 80, y - 80), (x + 80, y + 80), 15)
        pygame.draw.line(screen, BLACK, (x - 80, y + 80), (x + 80, y - 80), 15)

    def show_winner(winner: int) -> None:
        root = tk.Tk()
        font = ("Helvetica", 30)
        if order == 1:
            if winner == 1:
                text = "You lost!"
            elif winner == -1:
                text = "You win!"
            elif winner == 0:
                text = "No winner."
        elif order == -1:
            if winner == -1:
                text = "You lost!"
            elif winner == 1:
                text = "You win!"
            elif winner == 0:
                text = "No winner."
        label = tk.Label(root, text=text, font=font)
        label.pack(expand=True)
        root.mainloop()

    def predict() -> list:
        cs = cb.get_coordinate()
        pres: list = p_nn.predict([cb.get_formatted_chessboard()])[0].tolist()

        # MCTS
        cbb = copy.deepcopy(cb)
        cbb.set_flag()
        root = Node(copy.deepcopy(cbb), cbb.get_flag(), coordinate=None)
        for _ in range(0, 12000):
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
                    else:
                        current.set_value(cbb.get_winner() / 2 + 0.5)
                    while not (current.get_parent() is None):
                        current = current.get_parent()
                        s = 0
                        for i in current.get_children():
                            s = s + i.get_value() * i.get_time()
                        p = s / current.get_time()
                        current.set_value(p)
                    current.get_parent()

        for i in root.get_children():
            adds = 20 ** (i.get_value() - 0.4) - 0.3
            '''print(pres)'''
            pres[i.get_coordinate()[0] * 3 + i.get_coordinate()[1]] += adds * 1.5
            '''print(i.get_coordinate())
            print(i.get_value())
            print(adds)
        print(pres)'''

        max_p = 0
        for i in cs:
            if max_p <= pres[i[0] * 3 + i[1]]:
                max_p = pres[i[0] * 3 + i[1]]
                pre_out = i
        return pre_out

    '''Main'''
    screen.fill(WHITE)
    for i in range(0, 4):
        pygame.draw.line(screen, BLACK, (i * 600 // 3, 0), (i * 600 // 3, 600), 10)
        pygame.draw.line(screen, BLACK, (0, i * 600 // 3), (600, i * 600 // 3), 10)

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if order == -1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    #print(mouse_x, mouse_y)
                    h_pos = area_judgement(mouse_x, mouse_y)
                    cb.drop(h_pos)
                    #print(h_pos)
                    draw_circle(100 * (h_pos[0] * 2 + 1), 100 * (h_pos[1] * 2 + 1))
                    pygame.display.flip()
                    cb.judgement()
                    if cb.get_winner() != 0 or cb.is_full():
                        show_winner(cb.get_winner())
                        running = False
                        break
                    else:
                        order = order * (-1)
        if not running:
            break
        elif order == 1:
            c_pos = predict()
            cb.drop(c_pos)
            draw_cross(100 * (c_pos[0] * 2 + 1), 100 * (c_pos[1] * 2 + 1))
            pygame.display.flip()
            cb.judgement()
            if cb.get_winner() != 0 or cb.is_full():
                show_winner(cb.get_winner())
                break
            else:
                order = order * (-1)


        pygame.display.flip()


    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()