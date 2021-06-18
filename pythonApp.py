# -*- coding: utf-8 -*-

""" NUMERISCHE INTERPOLATION    * * *   Interpolation.py   * * *    Letzte Änderung am 15. Mai 2020   * * *

Anmerkung: Diese Python-App dient als Verständnishilfe zur Vorlesung "Numerik & Stochastik" bzw. "Numerische Grundlagen".

ANFORDERUNGEN: Python 3.x 
               Matplotlib, NumPy, SciPy 

Author: Rico Hartung                                  hartunro@ipvs.uni-stuttgart.de
Bugs fixed by: Prof. Dr. rer. nat. Dirk Pflüger       dirk.pflueger@ipvs.uni-stuttgart.de

Scientific Computing
Institut für parallele und verteilte Systeme
Universität Stuttgart                                                                                   """

import matplotlib
matplotlib.use('TkAgg')  # Auf manchen Geräten ist TkAgg schneller
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import tkinter as tk
from scipy.interpolate import interp1d
import sys
import os
import datetime


# --- --- --- Klassen und Methoden dieses Programms --- --- ---

# Klasse, die die Stützpunkte im Graphen verstellbar macht
class DraggableSupportingPoint(object):
    def __init__(self, artists, tolerance=5):
        for artist in artists:
            artist.set_picker(tolerance)
        self.artists = artists
        self.currently_dragging = False
        self.current_artist = None
        self.offset = (0, 0)

        for canvas in set(artist.figure.canvas for artist in self.artists):
            canvas.mpl_connect('button_press_event', self.on_press)
            canvas.mpl_connect('button_release_event', self.on_release)
            canvas.mpl_connect('pick_event', self.on_pick)
            canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        self.currently_dragging = True

    def on_release(self, event):
        update_plot()  # Aktualisiere den Graph
        if self.current_artist is not None:
            self.current_artist.figure.canvas.draw()
        self.currently_dragging = False
        self.current_artist = None

    def on_pick(self, event):
        if self.current_artist is None:
            self.current_artist = event.artist
            x0, y0 = event.artist.center
            x1, y1 = event.mouseevent.xdata, event.mouseevent.ydata
            self.offset = (x0 - x1), (y0 - y1)

    def on_motion(self, event):
        try:
            if not self.currently_dragging:
                return
            if self.current_artist is None:
                return
            dx, dy = self.offset
            self.current_artist.center = event.xdata + dx, event.ydata + dy
            self.current_artist.figure.canvas.draw()
            update_plot()  # Aktualisiere den Graph
        except TypeError:
            pass  # print('Bleibe innerhalb des Plot-Bereichs, um die Stützstelle zu verändern!')
        except:
            raise

    # Aktualisiere die Punkte im Graphen
    def update(self):
        self.current_artist = self.artists[0]
        self.current_artist.figure.canvas.draw()
        self.current_artist = None

    # Füge neuen Punkt hinzu, so dass dieser verstellbar wird (da n hier begrenzt ist, wird die Methode nicht genutzt)
    def add_artist(self, new_artist):
        self.artists = self.artists + [new_artist]


# Klasse des zusätzlichen Optionsfensters
class OptionsWindow:
    def __init__(self, master):
        # Aufbau des Zusatzfensters
        frame = tk.Frame(master)
        frame.pack()

        tk.Label(frame, text=' ').pack()
        self.p_info = tk.Label(frame, text=' ')
        self.p_info.pack()
        tk.Label(frame, text=' ').pack()
        self.addspButton = tk.Button(frame, text='+ Stützpunkt', command=lambda: change_nplus1(1), state='normal')
        self.addspButton.pack(fill='x')
        self.removespButton = tk.Button(frame, text='– Stützpunkt', command=lambda: change_nplus1(0))
        self.removespButton.pack(fill='x')
        tk.Label(frame, text=' ').pack()

        self.axes_v_var = tk.IntVar()
        self.axes_v = tk.Checkbutton(frame, text="Achsen hervorheben", variable=self.axes_v_var,
                                    command=lambda: showhide_a_func('axesv'))
        self.axes_v.pack(fill='x')
        self.axes_v.select()

        self.axes_s_var = tk.IntVar()
        self.axes_s = tk.Checkbutton(frame, text="Achsen anpassen", variable=self.axes_s_var,
                                    command=lambda: set_axes_s_var())
        self.axes_s.pack(fill='x')
        self.axes_s.select()

        tk.Label(frame, text=' ').pack()

        self.cb_gp_var = tk.IntVar()
        self.cb_gp = tk.Checkbutton(frame, text="globales Polynom", variable=self.cb_gp_var,
                                    command=lambda: showhide_a_func('glob'))
        self.cb_gp.pack(fill='x')
        self.cb_gp.select()

        self.cb_laguw_var = tk.IntVar()
        self.cb_laguw = tk.Checkbutton(frame, text="ungew. Lagrangepol.", variable=self.cb_laguw_var,
                                       command=lambda: showhide_a_func('laguw'))
        self.cb_laguw.pack(fill='x')
        self.cb_laguw.deselect()

        self.cb_lagw_var = tk.IntVar()
        self.cb_lagw = tk.Checkbutton(frame, text="gew. Lagrangepol.", variable=self.cb_lagw_var,
                                      command=lambda: showhide_a_func('lagw'))
        self.cb_lagw.pack(fill='x')
        self.cb_lagw.deselect()

        tk.Label(frame, text=' ').pack()

        self.cb_cs_var = tk.IntVar()
        self.cb_cs = tk.Checkbutton(frame, text="kubische Splines", variable=self.cb_cs_var,
                                    command=lambda: showhide_a_func('cub'))
        self.cb_cs.pack(fill='x')
        self.cb_cs.select()

        self.cb_cstang_var = tk.IntVar()
        self.cb_cstang = tk.Checkbutton(frame, text="Tangentengeraden", variable=self.cb_cstang_var,
                                      command=lambda: showhide_a_func('cubtang'))
        self.cb_cstang.pack(fill='x')
        self.cb_cstang.deselect()

        self.cb_csdx_var = tk.IntVar()
        self.cb_csdx = tk.Checkbutton(frame, text="Erste Ableitungen", variable=self.cb_csdx_var,
                                      command=lambda: showhide_a_func('cubdx'))
        self.cb_csdx.pack(fill='x')
        self.cb_csdx.deselect()

        self.cb_csdxx_var = tk.IntVar()
        self.cb_csdxx = tk.Checkbutton(frame, text="Zweite Ableitungen", variable=self.cb_csdxx_var,
                                       command=lambda: showhide_a_func('cubdxx'))
        self.cb_csdxx.pack(fill='x')
        self.cb_csdxx.deselect()

        tk.Label(frame, text=' ').pack()
        tk.Button(frame, text='Graph als PNG sichern', command=lambda: save_plot_to_png()).pack(fill='x')
        tk.Label(frame, text=' ').pack()
        tk.Button(frame, text='Programm neustarten', command=lambda: restart_program()).pack(fill='x')
        tk.Button(frame, text='Programm beenden', fg='black', command=frame.quit).pack(fill='x')

    # Wechselt den Zustand eines Knopfes (bzgl. der Stützpunkte)
    def change_button_state(self, button):
        if button == 1:
            if self.addspButton['state'] == 'normal':
                self.addspButton['state'] = 'disabled'
            else:
                self.addspButton['state'] = 'normal'
        if button == 2:
            if self.removespButton['state'] == 'normal':
                self.removespButton['state'] = 'disabled'
            else:
                self.removespButton['state'] = 'normal'

    # Veränderung der Polynombeschreibung
    def change_polynome_info(self, n):
        self.p_info['text'] = 'Grad(glob. Polynom) = ' + str(n)


# Neustart des kompletten Programms
def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


def set_axes_s_var():
    global setaxes_selected
    if setaxes_selected == 1:
            setaxes_selected = 0
    else:
        setaxes_selected = 1


def modify_canvas_limits(event):
    global plot_width, plot_height, setaxes_selectedm, lowerBound, upperBound, x_coeff, x
    if setaxes_selected == 1:
        w_size = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        if plot_width == 0:
            plot_width = w_size.width
            plot_height = w_size.height
        d1 = w_size.width - plot_width
        d2 = w_size.height - plot_height
        plot_width = w_size.width
        plot_height = w_size.height
        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()
        lowerBound = xmin - d1 * 2.54
        upperBound += d1 * 2.54
        x = np.linspace(lowerBound, upperBound, abs(upperBound - lowerBound) * x_coeff)  # Feinheit von x
        ax.set(xlim=[lowerBound, xmax], ylim=[ymin, ymax + d2 * 2.54])


# Entfernt alle Funktionen aus dem Graphen
def remove_ax_lines():
    global ax
    for _ in range(len(ax.lines), 0, -1):
        ax.lines.pop()


# Aktualisierung des Graphen
def update_plot():
    global X, Y, n, ax, p1, cs, cs_selected, cs_dx_selected, cs_dxx_selected, \
        la_uw_selected, la_w_selected, cs_tang_selected, axes_visible
    # Initialisierung von X und Y
    for i in range(0, n + 1):
        X[i], Y[i] = supporting_points[i].center

    # Reinige den Graphen
    remove_ax_lines()

    # Plotte ausgewählte Interpolanten
    if gp_selected == 1:  # globales Polynom
        gp = neville(X, Y)
        plt.plot(x, gp, '-', linewidth=2, color='orange', label='globales Polynom')
    if n > 2:  # Sonst können keine Splines mit SciPy berechnet werden
        if cs_selected or cs_dx_selected or cs_dxx_selected or cs_tang_selected:  # kubische Splines und deren Ableitungen
            cs = cubic_splines(X, Y)
            if cs_dx_selected or cs_dxx_selected or cs_tang_selected:
                dx = x[1]-x[0] # dx fuer aequidistante Punkte
                dcsdx = np.gradient(cs, dx)
                dcsdxx = np.gradient(dcsdx, dx)
                if cs_tang_selected:
                    T = tangents(X, Y, cs)
                    plt.plot(T[0][1], T[0][0], '-', linewidth=2, color=[0.4, 0.4, 0.4], label='Tangentengeraden')  # mit Label, f. Legende
                    [plt.plot(T[j][1], T[j][0], '-', linewidth=2, color=[0.4, 0.4, 0.4]) for j in range(1, n + 1)]
                if cs_dx_selected:
                    plt.plot(x, dcsdx, '--', linewidth=2, color=[0.4, 0.4, 0.4], label='1. Ableitungen der Splines')
                if cs_dxx_selected:
                    plt.plot(x, dcsdxx, '--', linewidth=2, color=[0.7, 0.7, 0.7], label='2. Ableitungen der Splines')
            if cs_selected:
                plt.plot(x, cs, '-', linewidth=2, color='r', label='kubische Splines')
    if la_uw_selected or la_w_selected:  # (un)gewichtete Lagrangepolynome
        L_unweighted, L_weighted = lagrange_polynomes(X, Y)
        legendcontrol1 = 0  # (*) Wir wollen beim Zeichnen nur ein Polynom mit dem label-Attribut,
        legendcontrol2 = 0  # da sonst (n+1) bzw. 2(n+1) gleiche Labels in der Legende vorkommen

        if la_uw_selected:
            cc = -1
            s = len(L_unweighted)
            for lagr in L_unweighted:
                cc += 1
                c = [float(s - cc)/float(s), 0.8, float(cc)/float(s)]  # RGB-Farbe (cc/s, 1, (s-cc)/s)
                if legendcontrol1 == 0:  # (*)
                    plt.plot(x, lagr, '--', linewidth=2, color=c, label='Lagrangepolynome (ungew.)')
                    legendcontrol1 = 1
                else:
                    plt.plot(x, lagr, '--', linewidth=2, color=c)
        if la_w_selected:
            cc = -1
            s = len(L_weighted)
            for lagr in L_weighted:
                cc += 1
                c = [float(s - cc)/float(s), 0.8, float(cc)/float(s)]  # RGB-Farbe (cc/s, 1, (s-cc)/s)
                if legendcontrol2 == 0:  # (*)
                    plt.plot(x, lagr, '-', linewidth=2, color=c, label='Lagrangepolynome (gew.)')
                    legendcontrol2 = 1
                else:
                    plt.plot(x, lagr, '-', linewidth=2, color=c)
    if axes_visible:
        ax.axhline(y=0, color=[0.6, 0.6, 0.6])
        ax.axvline(x=0, color=[0.6, 0.6, 0.6])

    # Aktualisiere die Legende des Graphen
    if not (gp_selected or cs_selected or cs_dx_selected or cs_dxx_selected or la_uw_selected or la_w_selected):
        plt.plot(x, x, '', color='white', label='keine Funktion ausgewählt')
        plt.legend()
        ax.lines[0].remove()
    else:
        plt.legend()


# Interpolation mittels Neville-Aitken-Schema (aus unserem Skript, Kap. 4, speicheropt. Algorithmus)
def neville(pX, Y):
    global n, x
    X = [a for a in pX]
    P = [a for a in Y]

    for k in range(1, n + 1):  # Durch alle Spalten (im Dreiecksschema)
        for i in range(n, k - 1, -1):  # Durch die Zeilen, Wiederverwendung der alten P_(i,k-1)-Variablen
            try:
                P[i] += ((x - X[i]) / (X[i] - X[i - k])) * (P[i] - P[i - 1])
            except RuntimeWarning:
                pass
    return P[n]


# Interpolation mit kubischen Splines (mit Hilfe der Bibliothek SciPy)
def cubic_splines(X, Y):
    global x
    sorted_X, sorted_Y = map(list, zip(*sorted(zip(X, Y), key=lambda t: t[0])))
    return interp1d(sorted_X, sorted_Y, bounds_error=False, kind='cubic', copy=True)(x) #, fill_value="extrapolate"


# Berechnung der (un)gewichteten Lagrangepolynomen; Gibt zwei Listen als Tupel zurück
def lagrange_polynomes(X, Y):
    global n
    L_unweighted = [lagrange(j, X) for j in range(0, n + 1)]
    L_weighted = [Y[i] * L_unweighted[i] for i in range(0, n + 1)]
    return L_unweighted, L_weighted


# Berechnung von l(j,n)
def lagrange(j, X):
    global n, x
    l = 1
    for i in range(0, n + 1):
        if i != j:
            l = l * (x - X[i]) / (X[j] - X[i])
    return l


# Berechnung der Tangenten in den Stützpunkten bezüglich der Splines
def tangents(X, Y, cs):
    global ax
    xmin, xmax = ax.get_xlim()
    d = (xmax - xmin) / 16
    return [tangent(X[j], Y[j], cs, d) for j in range(0, n + 1)]

# Berechnung einer speziellen Tangente in (a, fa)
def tangent(a, fa, cs, d):
    global x, x_coeff, lowerBound
    t = np.linspace(a - d, a + d, d * 2 * x_coeff)  # Feinheit für die Tangenten
    # delta between x-coords:
    dx = x[1]-x[0]
    m = np.gradient(cs, dx)
    return fa + m[np.int(np.floor((a + abs(lowerBound)) * x_coeff))] * (t - a), t

# Variation der Anzahl der Stützpunkte mit = { n-- falls i=0, n++ sonst     Achtung: n = Grad(Interpolant)
def change_nplus1(i):
    global n, ax, X, Y, options_window, n_max
    if i == 0:  # n--
        if n > 1:  # Falls es noch mehr als 2 Stützpunkte gibt
            n -= 1
            ax.patches.pop()
            X.pop()
            Y.pop()
            update_plot()
            fig.canvas.draw()
            #if n == n_max - 1:  # Falls n auf n_max-1 gesenkt wurde, dann schalte den Plus-Knopf wieder frei
            #    OptionsWindow.change_button_state(options_window, 1)
            #if n == 3:  # Falls n den kleinsten Wert erreicht hat, dann sperre den Minus-Knopf
            #    OptionsWindow.change_button_state(options_window, 2)
    else:  # n++
        if n < n_max:  # Falls die maximale Anzahl an Stützpunkten noch nicht erreicht wurde
            n += 1
            X.append(0)
            Y.append(0)
            ax.add_patch(supporting_points[n])
            update_plot()
            fig.canvas.draw()
            #if n == 4:  # Falls 5 SPe existieren, dann schalte den Minus-Knopf wieder frei
            #    OptionsWindow.change_button_state(options_window, 2)
            #if n == n_max:  # Falls n den maximalen Wert erreicht hat, dann sperre den Plus-Knopf
            #    OptionsWindow.change_button_state(options_window, 1)
    OptionsWindow.change_polynome_info(options_window, n)


# Speicherung des Graphen als PNG
def save_plot_to_png():
    plt.savefig('Graph {0}.png'.format(datetime.datetime.strftime(datetime.datetime.now(), '%y%m%d %H%M%S')))


# Anzeigen und Ausblenden von Funktionen im Graphen
def showhide_a_func(name):
    global options_window, gp_selected, cs_selected, cs_dx_selected, \
        cs_dxx_selected, la_uw_selected, la_w_selected, cs_tang_selected, axes_visible
    if name == 'axesv':
        if axes_visible == 1:
            axes_visible = 0
        else:
            axes_visible = 1
    if name == 'glob':
        if gp_selected == 1:
            gp_selected = 0
        else:
            gp_selected = 1
    if name == 'cub':
        if cs_selected == 1:
            cs_selected = 0
        else:
            cs_selected = 1
    if name == 'cubdx':
        if cs_dx_selected == 1:
            cs_dx_selected = 0
        else:
            cs_dx_selected = 1
    if name == 'cubdxx':
        if cs_dxx_selected == 1:
            cs_dxx_selected = 0
        else:
            cs_dxx_selected = 1
    if name == 'cubtang':
        if cs_tang_selected == 1:
            cs_tang_selected = 0
        else:
            cs_tang_selected = 1
    if name == 'laguw':
        if la_uw_selected == 1:
            la_uw_selected = 0
        else:
            la_uw_selected = 1
    if name == 'lagw':
        if la_w_selected == 1:
            la_w_selected = 0
        else:
            la_w_selected = 1
    update_plot()
    fig.canvas.draw()


# --- --- --- Definitionen und Initialisierungen, Einstellungen, GUI --- --- ---

np.seterr(divide='ignore', invalid='ignore')  # Ignoriere Meldungen des Typs RuntimeWarning

global ax
fig, ax = plt.subplots()
global x, lowerBound, upperBound, x_coeff
lowerBound = -4  # Nicht verändern!
upperBound = 12  # Nicht verändern!
x_coeff = 150  # Stellschraube für die Feinheit x; für eine höhere Genauigkeit größer wählen
x = np.linspace(lowerBound, upperBound, abs(upperBound - lowerBound) * x_coeff)  # Feinheit von x

rad = 0.12  # Radius der Kreise, welche die Stützpunkte darstellen
global n_max, n, supporting_points
n_max = 9  # Anzahl Stützpunkte - 1, Achtung: Beachte len(supporting_points).
n = n_max
supporting_points = [patches.Circle((-2, -1), rad, fc='red', alpha=0.5),
                     patches.Circle((3, 0), rad, fc='red', alpha=0.5),
                     patches.Circle((6, -1), rad, fc='red', alpha=0.5),
                     patches.Circle((8, 3), rad, fc='red', alpha=0.5),
                     patches.Circle((1, -2), rad, fc='red', alpha=0.5),
                     patches.Circle((7, -1), rad, fc='red', alpha=0.5),
                     patches.Circle((9, -2), rad, fc='red', alpha=0.5),
                     patches.Circle((-3, 0), rad, fc='red', alpha=0.5),
                     patches.Circle((0, 0), rad, fc='red', alpha=0.5),
                     patches.Circle((10, 1), rad, fc='red', alpha=0.5)]
for sp in supporting_points:  # Füge Stützpunkte zum Graphen hinzu
    ax.add_patch(sp)
global dsp
dsp = DraggableSupportingPoint(supporting_points)  # Mache Stützpunkte verstellbar

global X, Y
X = [0 for _ in range(0, n + 1)]  # Stützstellen
Y = [0 for _ in range(0, n + 1)]  # Stützwerte

# Auswahl der Funktionen, die beim Start angezeigt werden
global global_polynome_polynome, cs_selected, cs_dx_selected, cs_dxx_selected, \
    lagrange_polynomes_selected, cs_tang_selected, axes_visible, setaxes_selected
axes_visible = 1
setaxes_selected = 1
gp_selected = 1
lagrange_polynomes_selected = 0
la_uw_selected = 0
la_w_selected = 0
cs_selected = 1
cs_dx_selected = 0
cs_dxx_selected = 0
cs_tang_selected = 0

update_plot()  # Erstmaliges Aktualisieren des Graphen

# Einstellungen des Optionenfensters
root = tk.Tk()
global options_window, plot_width
options_window = OptionsWindow(root)
root.geometry('{}x{}'.format(230, 555))
root.title('Num. Interpolation')
#root.configure(background='white')
root.geometry("+%d+%d" % (30, 40))
OptionsWindow.change_polynome_info(options_window, n)

# Einstellungen des Graphenfensters
fig.canvas.set_window_title('Numerische Grundlagen: Interpolation')
# fig.set_size_inches(10, 8, True)
ax.set(xlim=[-4, 12], ylim=[-6, 6])
plot_width = 0
mngr = plt.get_current_fig_manager()
mngr.window.wm_geometry('+300+45')
ax.grid(True)
ax.axhline(y=0, color=[0.6, 0.6, 0.6])
ax.axvline(x=0, color=[0.6, 0.6, 0.6])
start, end = ax.get_ylim()
ax.yaxis.set_ticks(np.arange(start, end, 1))
fig.canvas.mpl_connect('resize_event', modify_canvas_limits)  # Veränderung der unteren u. oberen Graphengrenzen

plt.show()  # Zeige Hauptfenster, den Graphen
