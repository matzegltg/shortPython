import numpy.fft

# Hilfsfunktionen um Skript-FTs mit numpy FTs auszurechnen
# (die NumPy-Funktionen verwenden eine andere Skalierung
# als das Skript)
ifft = lambda x : numpy.fft.ifft(x)*len(x)
fft = lambda x : numpy.fft.fft(x)/len(x)

def polymult(u, v):
   """Polynommultiplikation
   
   Polynome dargestellt durch Liste oder Vektor p der Laenge N
   von Koeffizienten mittels 
   f(x) = p[0] + p[1]*x + p[2]*x**2 + ... + p[N-1]*x**(N-1)
   
   u, v -- Koeffizienten der Eingangspolynome
   Ergebnis: Koeffizienten von u * v
   """
   N = len(u) + len(v) - 1
   # Koeffizienten mit 0 auf Laenge des Ergebnisses auffuellen
   u.extend([0.]*(N - len(u)))
   v.extend([0.]*(N - len(v)))
   # An geeigneten Stellen auswerten
   print(f"u werte untransformiert = {u}")
   print(f"v werte untransformiert {v}")
   u_werte = ifft(u)
   print(f"uwerte + {u_werte}")
   v_werte = ifft(v)
   print(f"vwerte + {v_werte} ")
   # Komponenten weise multiplizieren
   w_werte = [u_werte[i]*v_werte[i] for i in range(N)]
   # ... und die Koeffizienten des Ergebnisses berechnen
   w = fft(w_werte)
   return w

if __name__ == '__main__':
    # Beispiel: (8x**2 + 4x + 2)*(-2x + 1) = -16x**3 + 2
    print([numpy.round(x,13) for x in polymult([2., 4., 8.], [1., -2.])])