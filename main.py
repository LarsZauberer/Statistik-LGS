import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as sc
import numpy as np
import math

st.title = "DIY vs. Numpy"

st.write("""
         # Ist DIY immer besser?
         
         ## Ist ein DIY LGS Algorithmus besser als ein professioneller LGS Algorithmus von Numpy?
         
         ## Motivation
         
         Es hat mich interessiert den Unterschied zwischen 2 Algorithmen etwas
         genauer unter die Lupe zu nehmen. Dabei hat es mich sehr interessiert,
         wie auch die wirkliche Zeit mit der Zeitkomplexität des Algorithmus
         zusammenhängt.
         
         Oft schreibe ich gerne einen Algorithmen selber, weil es eine gute
         Übung ist. Trotzdem verwende ich dann den Algorithmus. Deswegen wollte
         ich untersuchen wie viel Rechenzeit ich mit meinen Algorithmen
         verschwende.
         
         ## Daten
         
         Die Daten für diese Studie wurde simpl durch eine Python-Skript
         erstellt. Dabei gibt es einen simplen homemade Gaussalgorithmus,
         welcher ausgeführt wird, als auch einen LGS Algorithmus von Numpy.
         
         Bei den Matrizen handelt sich um ausschliesslich reguläre Matrizen.
         Diese müssen auch niemals permutiert werden, damit sie mit dem Gauss
         möglich werden.
         
         Bei der Berechnung wird die allgemeine Form von $A\\vec{x}=\\vec{b}$
         angewandt.
         """)

st.download_button("Download the data", "data.csv")

st.write("[Source Code auf GitHub](https://github.com/LarsZauberer/Statistik-LGS)")

# Load data.csv with panda
data = pd.read_csv("data.csv")

st.dataframe(data.head(10))

st.write("""
         ## Fragestellung
         
         In der Studie soll betrachtet werden, wie viel besser ein
         professioneller linearer Gleichungssystem Löser ist, als ein simpler,
         schnell gemachter Gauss Algorithmus.
         
         Dabei möchten wir auch auf die Fragestellung eingehen, wie viel Länger
         der Zeitaufwand wird bei steigender Grösse des Gleichungssystems.
         
         In der Studie soll nur auf den Zeitaufwand der Berechnung gehen und
         nicht um die CPU/RAM-Auslastung.
         
         ## Analyse
         
         ### Analyse der Komplexität
         
         """)   

noregress = st.button("Scatter Plots")
regress = st.button("Regression")

home = data.loc[data['algorithm'] == 'Homemade']
nump = data.loc[data['algorithm'] == 'Numpy']

m, q, r, *_ = sc.linregress(nump["matrix_size"], nump["time"])
model = np.poly1d(np.polyfit(home["matrix_size"], home["time"], 3))
a, b, c, d = np.polyfit(home["matrix_size"], home["time"], 3)

if noregress or (noregress == False and regress == False):
    fig, ax = plt.subplots()
    ax.plot(home["matrix_size"], home["time"], "o", label="Homemade")
    ax.plot(nump["matrix_size"], nump["time"], "o", label="Numpy")
    ax.set_xlabel("Matrixgrösse")
    ax.set_ylabel("Zeit")
    ax.legend()
    st.pyplot(fig)
if regress:
    fig, ax = plt.subplots()
    polyline = np.linspace(1, 100)
    ax.plot(polyline, model(polyline), label=f"Homemade")
    ax.plot(nump["matrix_size"], (m * nump["matrix_size"]) + q, label=f"Numpy r={r:.2f}")
    ax.set_xlabel("Matrixgrösse")
    ax.set_ylabel("Zeit")
    ax.legend()
    st.pyplot(fig)

st.write(f"""
         Hier kann gut gesehen werden, der zeitliche Unterschied zwischen den
         Funktionen in bezug auf die Komplexität. Man sieht nur einen sehr
         leichten anstieg in Numpy mit einer Regressionsfunktion $f(x) = {m:.5f}x + {q:.5f}$.
         
         Der DIY Algorithmus hat dagegen eine eher höhere Steigung mit
         zunehmender Komplexität. Die Komplexität ist eher kubisch. Das liegt
         daran, dass die Funktion zur berechnung der Dreiecksmatrix eine
         Zeitkomplexität von $O(n^3)$ ausweist. Die Regressionsfunktion ist $f(x) = {a:.5f}x^3 + {b:.5f}x^2 + {c:.5f}x + {d:.5f}$.
         
         ---
         """)

fig, ax = plt.subplots()
ax.plot(home["matrix_size"], np.log(home["time"]), "o", label=f"log(Homemade)")
ax.set_xlabel("Matrixgrösse")
ax.set_ylabel("Zeit")
ax.legend()
st.pyplot(fig)

st.write(f"""
         Das ist die logarithmische Zeit des homemade Algorithmus. Da diese
         Kurve nicht linear ist, kann man sehen, dass die Funktion nicht exponentiell sein kann.
         """)

st.write(f"""
         ---
         
         Jetzt gibt es auch noch viele ausreisser. Nun wäre es noch interessant
         herauszufinden, bei welcher Komplexität, welcher Algorithmus wie lange
         braucht.
         """)

meansHome = []
for i in range(100):
    meansHome.append(home.loc[home["matrix_size"] == i]["time"].mean())
meansNump = []
for i in range(100):
    meansNump.append(nump.loc[nump["matrix_size"] == i]["time"].mean())

fig, ax = plt.subplots()
ax.plot(range(100), meansHome, label=f"Durschnitt Homemade")
ax.plot(range(100), meansNump, label=f"Durschnitt Homemade")
ax.set_xlabel("Matrixgrösse")
ax.set_ylabel("Zeit")
ax.legend()
st.pyplot(fig)

st.write(f"""
         Man kann eine sehr grosse Schwankung in den Kurven erkennen. Das liegt
         wahrscheinlich an den zufälliggenerierten Daten. Dabei entstehen nicht
         immer gleich schwere Gleichungssysteme.
         """)

x = st.slider("Matrixgrösse für Numpy", 0, 100, 10)

st.write(f"""
         Numpy bräuchte für eine Matrixgrösse von **{x}** eine Zeit von
         **{nump.loc[nump["matrix_size"] == x]["time"].mean():.2f}** Sekunden.
         """)

x = st.slider("Matrixgrösse für den Homemade Algorithmus", 0, 100, 10)

st.write(f"""
         Der Homemade Algorithmus bräuchte für eine Matrixgrösse von **{x}**
         eine Zeit von **{home.loc[home["matrix_size"] ==
         x]["time"].mean():.2f}** Sekunden.
         """)

st.write(f"""
         ---
         
         ## Fazit
         
         Für sehr kleine Matrizen ist ein selbstgemachter Algorithmus fast genau
         gleich schnell. Sobald die Gleichungssysteme einen grossen Ausmass
         annehmen sind optimierte Lineare Gleichungssysteme von Nöten, damit die
         zeitliche Verwendung nicht die Überhand übernimmt.
         
         Wenn die Implementierung eines professionellen Algorithmus nicht zu
         aufwendig ist, dann ist es zu empfehlen einen solchen zu verwenden. Man
         spart Zeit und in der Ausführung ist der Algorithmus auch einiges
         schneller.
         
         ---
         
         ## Algorithmen selber testen
         """)

A = st.text_input("""Gib eine Matrix im Octave Format ein. (Bsp.
              [1,2,3;4,5,6;7,8,9]). Bedenke, dass die Matrix regulär sein muss,
              damit sie gelöst werden kann.""", value="[2,1,0;0,3,2;2,4,10]")

b = st.text_input("""
                  Gib einen Wert für den Vektor b ein. Bsp. [1,2,3]
                  """, value=[21,15,12])

try:
    AMat = []
    for i in A.split(";"):
        i = i.replace("[", "").replace("]", "").replace(" ", "")
        i = i.split(",")
        i = [int(j) for j in i]
        AMat.append(i)

    latexMatrix = "\\begin{pmatrix}"
    for i in AMat:
        for e in i:
            if e == i[-1]:
                latexMatrix += f"{e}"
                continue
            latexMatrix += f"{e} && "
        latexMatrix += "\\\\"
    latexMatrix += "\\end{pmatrix}"
    
    latexB = "\\begin{pmatrix}"
    b = b.replace("[", "").replace("]", "").replace(" ", "")
    for i in b.split(","):
        if i == b.split(",")[-1]:
            latexB += f"{i}"
            continue
        latexB += f"{i} \\\\"
    latexB += "\\end{pmatrix}"
    
    st.latex(latexMatrix + "\\vec{x} = " + latexB)
    
    from src.larsalgo import Problem
    import time
    b = [int(i) for i in b.split(",")]
    p = Problem(AMat, b)
    t = time.time()
    p.solve()
    t1 = time.time() - t
    print(p.x)
    x = str(p.x)
    
    latexX = "\\begin{pmatrix}"
    x = x.replace("[", "").replace("]", "").replace(" ", "")
    for i in x.split(","):
        if i == x.split(",")[-1]:
            latexX += f"{i}"
            continue
        latexX += f"{i} \\\\"
    latexX += "\\end{pmatrix}"
    
    st.latex("\\vec{x} = " + latexX)
    
    # Calculate numpy
    import numpy as np
    A = np.array(AMat)
    b = np.array(b)
    t = time.time()
    np.linalg.solve(A, b)
    t2 = time.time() - t
    
    st.write(f"""
             Der Homemade Algorithmus hat {t1:.5f} Sekunden gebraucht.
             """)
    
    st.write(f"""
             Der Numpy Algorithmus hat {t2:.5f} Sekunden gebraucht.
             """)
    
except Exception as e:
    print(e)
    st.write("Das ist keine gültige Matrix.")
