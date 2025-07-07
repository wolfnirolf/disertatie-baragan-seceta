import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 1. Încarcă datele
df = pd.read_excel("Date-6statii-precipitatii.xlsx")

# 2. Redenumire coloane
df.rename(columns={"An_numeric": "An", "Luna_numeric": "Luna"}, inplace=True)

# 3. Clasificare Hellmann
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

# 4. Media regională lunară
media = df.groupby(["An", "Luna"])["Scor_Hellmann"].mean().unstack()

# 5. Heatmap
plt.figure(figsize=(9, 12))
sns.heatmap(
    media,
    cmap=sns.color_palette("RdYlBu_r", as_cmap=True),
    linewidths=0.1,
    linecolor='white',
    cbar_kws={'label': 'Scor mediu Hellmann'},
    square=False
)

plt.title("Distribuția lunară a clasificării Hellmann în Câmpia Bărăganului\n(1961–2020, medie regională pe stații)", fontsize=13)
plt.xlabel("- Luna -", fontsize=11)
plt.ylabel("- Anul -", fontsize=11)
plt.xticks(ticks=np.arange(12) + 0.5, labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], rotation=0)
plt.yticks(rotation=0, fontweight='bold')
plt.tight_layout()

# 6. Salvare
plt.savefig("heatmap_hellmann_baragan.png", dpi=300)
plt.show()
