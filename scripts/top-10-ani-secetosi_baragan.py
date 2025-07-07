import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm
import matplotlib.patheffects as path_effects
import numpy as np

# Încarcă datele
df = pd.read_excel("Date_6statii_cu_scor_hellmann_lunar.xlsx")

# Calculează scorul mediu anual pentru fiecare stație
annual_scores = df.groupby(['Statie', 'An_numeric'])['hellmann_score_lunar'].mean().reset_index()
annual_scores.rename(columns={'hellmann_score_lunar': 'scor_hellmann_mediu_anual'}, inplace=True)

# Media anuală pe toate stațiile
mean_scores = annual_scores.groupby('An_numeric')['scor_hellmann_mediu_anual'].mean().reset_index()

# Top 10 cei mai secetoși ani
top10 = mean_scores.sort_values(by='scor_hellmann_mediu_anual', ascending=False).head(10).sort_values('An_numeric')

# Normalizează valorile pentru maparea culorilor
norm = plt.Normalize(top10['scor_hellmann_mediu_anual'].min(), top10['scor_hellmann_mediu_anual'].max())
colors = [cm.YlOrBr(norm(val)) for val in top10['scor_hellmann_mediu_anual']]

# Creează graficul
plt.figure(figsize=(10, 6))
bars = plt.bar(
    top10['An_numeric'].astype(str),
    top10['scor_hellmann_mediu_anual'],
    color=colors,
    edgecolor='black',
    linewidth=1
)

# Adaugă valori pe bare cu contur negru
for bar, value in zip(bars, top10['scor_hellmann_mediu_anual']):
    txt = plt.text(bar.get_x() + bar.get_width() / 2,
                   bar.get_height() - 0.03,
                   f"{value:.2f}",
                   ha='center',
                   va='top',
                   color='white',
                   fontsize=9,
                   fontweight='bold')
    txt.set_path_effects([path_effects.Stroke(linewidth=1, foreground='black'),
                          path_effects.Normal()])

# Titlu și etichete
plt.title("Top 10 cei mai secetoși ani în Câmpia Bărăganului\n(scor mediu anual de severitate Hellmann 1961–2020)", fontsize=13)
plt.xlabel("Anul", fontsize=11)
plt.ylabel("Scor mediu anual de severitate", fontsize=11)

# Poziționează legenda deasupra anilor 1994 și 2000 (coloanele 6 și 7 din cele 10)
plt.text(5.6, 1.42, "Scoruri Hellmann:\n2 = Excesiv secetoasă\n1 = Secetoasă / Moderat\n0 = Altele",
         fontsize=9, verticalalignment='top',
         bbox=dict(boxstyle="round", facecolor="white", edgecolor="gray"))

plt.tight_layout()
plt.savefig("grafic_top-10-ani-secetosi_baragan.png", dpi=300)
print("Grafic salvat ca 'grafic_top-10-ani-secetosi_baragan.png'")
