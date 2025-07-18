
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

# 1. Încarcă datele
df = pd.read_excel("Date-6statii-precipitatii.xlsx")
df.rename(columns={"An_numeric": "An", "Luna_numeric": "Luna"}, inplace=True)

# 2. Clasificare Hellmann numerică
def scor_hellmann(p):
    if p < 5:
        return 1
    elif p < 10:
        return 2
    elif p < 20:
        return 3
    elif p < 40:
        return 4
    elif p < 60:
        return 5
    else:
        return 6

df["Scor_Hellmann"] = df["precip_total"].apply(scor_hellmann)

# 3. Media regională lunară
media = df.groupby(["An", "Luna"])["Scor_Hellmann"].mean().unstack()

# 4. Heatmap cu colorbar
plt.figure(figsize=(9, 12))
cmap = sns.color_palette("RdYlBu_r", as_cmap=True)
sns.heatmap(
    media,
    cmap=cmap,
    linewidths=0.1,
    linecolor='white',
    cbar=True,
    cbar_kws={'label': 'Scor mediu Hellmann'},
    square=False,
    vmin=1, vmax=6
)

plt.title("Distribuția lunară a clasificării Hellmann în Câmpia Bărăganului\n(1961–2020, medie regională pe stații)", fontsize=13)
plt.xlabel("Lună", fontsize=11)
plt.ylabel("An", fontsize=11)
plt.xticks(
    ticks=np.arange(12) + 0.5,
    labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    rotation=0
)
plt.yticks(rotation=0, fontweight='bold')

# 5. Legendă cu scoruri 6–1 și culori din colormap în ordine inversă
etichete = [
    "Excesiv secetoasă", "Secetoasă", "Moderat secetoasă",
    "Normală", "Umedă", "Excesiv umedă"
]
norm = Normalize(vmin=1, vmax=6)
sm = ScalarMappable(norm=norm, cmap=cmap)
colors = [sm.to_rgba(i) for i in range(6, 0, -1)]  # de la 6 la 1
patches = [mpatches.Patch(color=colors[i], label=etichete[i]) for i in range(6)]

plt.legend(
    handles=patches,
    title="Clasificare Hellmann",
    loc='upper center',
    bbox_to_anchor=(0.5, -0.04),
    ncol=3,
    frameon=True,
    fancybox=False,
    borderpad=0.8,
    edgecolor='black'
)

# 6. Salvare
plt.savefig("grafic_heatmap_hellmann_campia_baraganului.png", dpi=300, bbox_inches='tight')
plt.show()
