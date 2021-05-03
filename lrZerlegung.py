# -*- coding: utf-8 -*-

""" LINERARE GLEICHUNGSSYSTEME          * * *   LR.py   * * *       Letzte Änderung am 08.11.2016   * * *

Anmerkung: Diese Python-App dient als Verständnishilfe zur Vorlesung "Numerische Grundlagen".

ANFORDERUNGEN: Python 3.x (getestet mit v3.5)

Rico Hartung                             hartunro@ipvs.uni-stuttgart.de
Prof. Dr. rer. nat. Dirk Pflüger         dirk.pflueger@ipvs.uni-stuttgart.de

Simulation großer Systeme
Institut für parallele und verteilte Systeme
Universität Stuttgart                                                                                   """

from tkinter import Tk, Menu, Label, Entry, Text, Button, Frame, LEFT, CENTER, TOP, END, X
import sys
import os


# HAUPTFENSTER   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

class LU(Tk):
    fontsize = 23
    
    def __init__(self, fontsize=fontsize):
        Tk.__init__(self)
        self.title('LR-Zerlegung')
        self.Cont = Button(self, text='Nächster Schritt >', command=lambda: stepByStepSolver(), state='normal')
        self.Cont.grid(row=9, column=2, pady=10, columnspan=11)
        self.Cont.config(font=("Courier", 13))
        self.Start = Button(self, text='<< Zurücksetzen', command=lambda: reset(), state='normal')
        self.Start.grid(row=9, column=1, pady=10, columnspan=6)
        self.Start.config(font=("Courier", 13))
        self.Operation1 = Label(self, text='[Derzeitige Rechenoperation]')
        self.Operation1.grid(row=7, pady=5, columnspan=12)
        self.Operation1.config(font=("Courier", fontsize))
        self.Operation2 = Label(self, text='[Nächste Rechenoperation]')
        self.Operation2.grid(row=8, pady=5, columnspan=12)
        self.Operation2.config(font=("Courier", fontsize))
        # self.Back.grid(row=7, column=4, pady=30)
        self.L = [e[:] for e in [[0] * 5] * 5]
        self.U = [e[:] for e in [[0] * 5] * 5]
        for i in range(0, 5):
            self.L[i][i] = 1

        # Markierungen
        self.m_kj = [e for e in range(0, 5)]
        for i in range(0, 5):
            self.m_kj[i] = Label(self, text=' ')
            self.m_kj[i].grid(row=6, column=i + 6, padx=0, pady=10)
            self.m_kj[i].config(font=("Courier", fontsize))
        self.m_i = [e for e in range(0, 5)]
        for i in range(0, 5):
            self.m_i[i] = Label(self, text=' ')
            self.m_i[i].grid(row=i, column=12, padx=15, pady=10)
            self.m_i[i].config(font=("Courier", fontsize))

        # Zellen initialisieren
        for j in range(0, 5):  # über die Spalten
            for i in range(0, 5):  # über die Zeilen
                if j == i:
                    self.L[i][j] = Entry(self, width=4)
                    self.L[i][j].grid(row=i, column=j, padx=3, pady=10)
                    self.L[i][j].insert('1', '1.0')
                    self.L[i][j].config(font=("Courier", fontsize))
                else:
                    self.L[i][j] = Entry(self, width=4)
                    self.L[i][j].grid(row=i, column=j, padx=3, pady=10)
                    self.L[i][j].insert('1', '0.0')
                    self.L[i][j].config(font=("Courier", fontsize))

        mult_dot = Label(self, text='*')
        mult_dot.grid(row=2, column=5, padx=20, pady=10)
        mult_dot.config(font=("Courier", fontsize))

        for j in range(0, 5):  # über die Spalten
            for i in range(0, 5):  # über die Zeilen
                self.U[i][j] = Entry(self, width=4)
                self.U[i][j].grid(row=i, column=j + 6, padx=3, pady=10)
                self.U[i][j].insert('1', '1.0')
                self.U[i][j].config(font=("Courier", fontsize))

    def config_U(self, c):
        """ Konfiguration der Matrix U """
        self.set_kij(0, 1, 0)
        for j in range(0, 5):  # über die Spalten
            for i in range(0, 5):  # über die Zeilen
                e = config[i][j]
                self.set_U(i, j, e)

    def reset_L(self):
        """ Zurücksetzen der Matrix L """
        for j in range(0, 5):  # über die Spalten
            for i in range(0, 5):  # über die Zeilen
                if i == j:
                    self.set_L(i, j, 1.0)
                else:
                    self.set_L(i, j, 0.0)

    def get_L(self, i, j):
        return self.L[i][j].get()

    def get_U(self, i, j):
        return self.U[i][j].get()

    def set_L(self, i, j, v):
        self.L[i][j].delete(0, END)
        self.L[i][j].insert(0, v)

    def set_U(self, i, j, v):
        self.U[i][j].delete(0, END)
        self.U[i][j].insert(0, v)

    def reset_all_colours(self):
        for j in range(0, 5):
            for i in range(0, 5):
                self.L[i][j].config(background='white', highlightbackground='white')
                self.U[i][j].config(background='white', highlightbackground='white')

    def set_colours(self, k, i, j):
        if i < 5 and k is not 4:
            for q in range(k, 5):
                self.U[i][q].config(background='yellow')
            if j < 5:
                self.U[i][j].config(highlightbackground='red')
                self.U[k][j].config(highlightbackground='red')
            self.U[k][k].config(background='green')
            self.U[i][k].config(background='green')
            self.L[i][k].config(background='green')

    def set_operations(self, k, i, j):
        k_n, i_n, j_n = k, i, j + 1
        if i == 5 and k < 5 and j == 5:
            k_n = k + 1
            i_n = k + 2
            j_n = k + 1
        if j == 5 and i < 5:
            i_n = i + 1
            j_n = k
        op_now = 'Derzeitiger Schritt: A(' + str(i) + ',' + str(j) + ') =  A(' + str(i) + ',' + str(j) + \
                 ') - L(' + str(i) + ',' + str(k) + ') * A(' + str(k) + ',' + str(j) + ')'
        self.Operation1['text'] = op_now
        self.Operation1.config(foreground='red')
        if k_n < 5:
            op_next = 'Nächster Schritt: A(' + str(i_n) + ',' + str(j_n) + ') =  A(' + str(i_n) + ',' + str(j_n) + \
                        ') - L(' + str(i_n) + ',' + str(k_n) + ') * A(' + str(k_n) + ',' + str(j_n) + ')'
            self.Operation2['text'] = op_next
            self.U[i_n-1][j_n-1].config(highlightbackground='gray')
            self.U[k_n-1][j_n-1].config(highlightbackground='gray')
            self.Operation2.config(foreground='black')
        else:
            op_next = '- - -'
            self.Operation2['text'] = op_next
            self.Operation2.config(foreground='gray')

    def set_kij(self, k, i, j):
        if j < 5:
            self.set_operations(k + 1, i + 1, j + 1)
        for q in range(0, 5):
            self.m_i[q]['text'] = ''
            self.m_kj[q]['text'] = ''
        if i < 5:
            self.m_i[i]['text'] = 'i'
        if k is not j:  # Achtung: Innerhalb des Algorithmus ist die Reihenfolge vertauscht.
            if k < 5:
                self.m_kj[k]['text'] = 'j'
            if j < 5:
                self.m_kj[j]['text'] = 'k'
        else:
            if k < 5:
                self.m_kj[k]['text'] = 'j k'


# LÖSUNGSVERFAHREN   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

def LU_factorisation_step():
    """ Ausführung eines Schrittes der LR-Zerlegung """
    global k, i, j
    for k_ in range(k, 5):
        for i_ in range(i, 5):
            if j == k:
                new = U(i_, k_) / U(k_, k_)
                L(i_, k_, new)
                U(i_, k_, 0)
                j += 1
                return
            for j_ in range(j, 5):
                new = U(i_, j_) - L(i_, k_) * U(k_, j_)
                U(i_, j_, new)
                j += 1
                if j_ < 4:
                    return
            i += 1
            j = k
            if i_ < 4:
                    return
        k += 1
        i = k + 1
        j = k
        if k_ < 3:
            return
    return


# HAUPTPROGRAMM   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

def num(v):
    """ Text-zu-Zahl-Konvertierung """
    try:
        return float(v)
    except ValueError:
        print('Falsche Eingabe!')


def L(i, j, v=None):
    """ Rückgabe/Setzen des Eintrags (i,j) aus L """
    if v is None:
        return num(LU.get_L(mat, i, j))
    else:
        LU.set_L(mat, i, j, v)


def U(i, j, v=None):
    """ Rückgabe/Setzen des Eintrags (i,j) aus U """
    if v is None:
        return num(LU.get_U(mat, i, j))
    else:
        LU.set_U(mat, i, j, v)


def stepByStepSolver():
    """ Führt nötige Methoden für einen Schritt aus """
    global mat, k, i, j
    if i is not 5:
        LU.reset_all_colours(mat)
    LU.set_colours(mat, k, i, j)
    if i < 5:
        LU.set_kij(mat, k, i, j)
    LU_factorisation_step()


def reset():
    global mat, k, i, j, z, config
    k = 0
    i = k + 1
    j = k
    z = 0
    LU.reset_L(mat)
    LU.config_U(mat, config)
    LU.reset_all_colours(mat)
    LU.set_kij(mat, k, i, j)


global mat, k, i, j, config
k = 0
i = k + 1
j = k
config = [[1.0, 2.0, 3.0, 4.0, 5.0],
          [1.0, 4.0, 8.0, 9.0, 10.0],
          [1.0, 4.0, 16.0, 24.0, 30.0],
          [1.0, 4.0, 16.0, 48.0, 60.0],
          [1.0, 4.0, 16.0, 48.0, 120.0]]
config = [[1.0, 2.0, 3.0, 4.0, 5.0],
          [2.0, 8.0, 16.0, 18.0, 20.0],
          [2.0, 8.0, 32.0, 48.0, 60.0],
          [3.0, 12.0, 48.0, 144.0, 180.0],
          [4.0, 16.0, 64.0, 192.0, 480.0]]

mat = LU()
LU.config_U(mat, config)

mat.mainloop()
