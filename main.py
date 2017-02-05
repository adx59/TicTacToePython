#!/usr/bin/env python

"""TicTacToe with a crappy computer player. It can also be played in two-player."""

__author__ = 'Adam Xu(adx59)'

from tkinter import *
from tkinter import messagebox
import random


class tCell(Button):
    def __init__(self, coords, master):
        Button.__init__(self, text = '', relief = 'groove', width = 8, height = 4, command = self.mark)
        self.x = coords[0]
        self.y = coords[1]
        self.master = master
        self.grid(row = coords[0], column = coords[1])
        self.marked = False
        self.letter = ''

    def __str__(self):
        return self.letter

    def mark(self):
        if not self.marked:
            if self.master.mode == "X":
                self.master.count += 1
                self.markX()
                self.master.mode = "O"
                self.master.refresh()
            elif self.master.mode == "O":
                self.master.count += 1
                self.markO()
                self.master.mode = "X"
                self.master.refresh()

    def markX(self):
        self['text'] = 'X'
        self.letter = 'X'
        self.marked = True
        if self.master.checkWin() == 'X':
            self.master.win('X')
        elif self.master.checkWin() == 'Tie':
            self.master.tie()

    def markO(self):
        self['text'] = 'O'
        self.letter = 'O'
        self.marked = True
        if self.master.checkWin() == 'O':
            self.master.win('O')
        elif self.master.checkWin() == 'Tie':
            self.master.tie()

    def unMark(self):
        self.marked = False
        self.letter = ''
        self['text'] = ''

class tGrid(Frame):
    def __init__(self, master):
        self.mode = 'X'
        self.cells = [['','',''],['','',''],['','','']]
        self.count = 0
        Frame.__init__(self, master)
        self.modeLbl = Label(text = "X", font = ('Comic Sans MS', 15))
        self.AIbutton = Button(text = "CPT", relief = "groove", width = 8, height = 2, bg = "yellow", command = self.cpMove)
        for x in range(3):
            for y in range(3):
                self.cells[x][y] = tCell((x, y), self)

        self.AIbutton.grid(row = 5, column = 1)
        self.modeLbl.grid(row = 4, column = 1)
        self.cols = [['', '', ''], ['', '', ''], ['', '', '']]
        for a in range(3):
            self.cols[a][0] = self.cells[0][a]
            self.cols[a][1] = self.cells[1][a]
            self.cols[a][2] = self.cells[2][a]
        self.diag = [[self.cells[0][0], self.cells[1][1], self.cells[2][2]], [self.cells[0][2], self.cells[1][1], self.cells[2][0]]]

    def refresh(self):
        self.modeLbl['text'] = self.mode
        self.cols = [['', '', ''], ['', '', ''], ['', '', '']]
        for a in range(3):
            self.cols[a][0] = self.cells[0][a]
            self.cols[a][1] = self.cells[1][a]
            self.cols[a][2] = self.cells[2][a]
        self.diag = [
            [self.cells[0][0], self.cells[1][1], self.cells[2][2]],
            [self.cells[0][2], self.cells[1][1], self.cells[2][0]]
        ]


    def checkWin(self):
        """g.checkWin -> bool or str
            returns false if no one has won on the board
            if all the board is filled up, returns tie.
            else, it returns the winner's letter"""
        self.refresh()
        for a in self.cells:
            if a[0].letter == a[1].letter == a[2].letter and a[0].marked == True:
                return a[0].letter
        for b in self.cols:
            if b[0].letter == b[1].letter == b[2].letter and b[0].marked == True:
                return b[0].letter
        for c in self.diag:
            if c[0].letter == c[1].letter == c[2].letter and c[0].marked == True:
                return c[0].letter
        if self.count == 9:
            return 'Tie'
        return False

    def tie(self):
        """g.tie -> None
            tells the player it's a tie and exits
            the program."""
        messagebox.showinfo('TicTacToe', 'Tie!')
        sys.exit()

    def cpMove(self):
        """g.cpMove -> None
            marks the board where it thinks it's the best
            spot. The computer player is extremely defensive
            instead of aggressive."""
        # be prepared for some crap quality code with ambiguous names and horrible planning
        self.refresh()
        bestCell = [[0, 0], 0]
        for a in self.cells:
            for b in a:
                if b.marked:
                    continue
                else:
                    b.letter = self.mode
                    b.marked = True
                    for c in self.cells:
                        occ = 0
                        if b in c:
                            o = 0
                            for x in c:
                                if x.letter == self.mode:
                                    o += 1
                            if o >= 2:
                                occ += 1
                        if occ > bestCell[1]:
                            bestCell = [[b.x, b.y], occ]
                    for d in self.cols:
                        occ = 0
                        if b in d:
                            o = 0
                            for x in d:
                                if x.letter == self.mode:
                                    o += 1
                            if o >= 2:
                                occ += 1
                        if occ > bestCell[1]:
                            bestCell = [[b.x, b.y], occ]
                    for e in self.diag:
                        occ = 0
                        if b in e:
                            o = 0
                            for x in e:
                                if x.letter == self.mode:
                                    o += 1
                            if o >= 2:
                                occ += 1
                        if occ > bestCell[1]:
                            bestCell = [[b.x, b.y], occ]
                    #"unmark" the cell
                    b.marked = False
                    b.letter = ''

        for a in self.cells:
            amntMarked = 0
            amtMarkedW = 0
            for cell in a:
                if cell.marked and cell.letter != self.mode:
                    amntMarked += 1
                if cell.marked and cell.letter == self.mode:
                    amtMarkedW += 1
            if amtMarkedW == 2:
                for cell in a:
                    if not cell.marked:
                        bestCell = [[cell.x, cell.y], 0]
            if amntMarked == 2:
                for cell in a:
                    if not cell.marked:
                        bestCell = [[cell.x, cell.y], 0]
        for b in self.cols:
            amntMarked = 0
            amtMarkedW = 0
            for cell in b:
                if cell.marked and cell.letter != self.mode:
                    amntMarked += 1
                if cell.marked and cell.letter == self.mode:
                    amtMarkedW += 1
            if amtMarkedW == 2:
                for cell in b:
                    if not cell.marked:
                        bestCell = [[cell.x, cell.y], 0]
            if amntMarked == 2:
                for cell in b:
                    if not cell.marked:
                        bestCell = [[cell.x, cell.y], 0]
        for c in self.diag:
            amntMarked = 0
            amtMarkedW = 0
            for cell in c:
                if cell.marked and cell.letter != self.mode:
                    amntMarked += 1
                if cell.marked and cell.letter == self.mode:
                    amtMarkedW += 1
            if amtMarkedW == 2:
                for cell in c:
                    if not cell.marked:
                        bestCell = [[cell.x, cell.y], 0]
            elif amntMarked == 2:
                for cell in c:
                    if not cell.marked:
                        bestCell = [[cell.x, cell.y], 0]

        if bestCell == [[0, 0], 0]:
            bestCell[0][0] = random.randrange(3)
            bestCell[0][1] = random.randrange(3)
            while self.cells[bestCell[0][0]][bestCell[0][1]].marked == True:
                bestCell[0][0] = random.randrange(3)
                bestCell[0][1] = random.randrange(3)

        self.cells[bestCell[0][0]][bestCell[0][1]].mark()

    def win(self, letter):
        messagebox.showinfo("TicTacToe", letter + " wins!")
        sys.exit()

    def cust(self, color, width):
        for row in self.cells:
            for cell in row:
                cell['bg'] = color
                cell['borderwidth'] = width




root = Tk()
root.title("TTT")
root.iconbitmap('favicon.ico')
grid = tGrid(root)

def custBoard():
    bwidth = IntVar()
    bentry = Entry(textvariable = bwidth, width = 7).grid(row = 7, column = 2)
    blabel = Label(text = 'BWidth').grid(row = 7, column = 0)
    bcolor = StringVar()
    centry = Entry(textvariable = bcolor, width = 7).grid(row = 8, column = 2)
    clabel = Label(text = 'CColor').grid(row = 8, column = 0)
    def updte():
        grid.cust(bcolor.get(), bwidth.get())
    update = Button(command = updte, text = 'Update', height = 1, relief = 'groove', bg = 'green').grid(row = 9, column = 1)

cust = Button(text = 'CBoard', relief = 'groove', width = 7, height = 1, bg = 'red', command = custBoard).grid(row = 6, column = 1)

root.mainloop()

