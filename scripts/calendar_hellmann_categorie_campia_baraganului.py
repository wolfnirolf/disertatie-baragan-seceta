import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches

# 1. Încarcă datele
df = pd.read_excel("Date-statii-precipitatii.xlsx")
df.rename(columns={"An_numeric": "An", "Luna_numeric": "Luna"}, inplace=True)

# 2. Clasificare Hellmann
def clasificare_hellmann(p):
    if p < 5:
        return "Excesiv secetoasă"
    elif p < 10:
        return "Secetoasă"
    elif p < 20:
        return "Moderat secetoasă"
    elif p < 40:
        return "Normală"
    elif p < 60:
        return "Umedă"
    elif p < 100:
        return "Foarte umedă"
    else:
        return "Excesiv umedă"

df["Clasa_Hellmann"] = df["precip_total"].apply(clasificare_hellmann)

# 3. Ordine și paletă roșu-albastru
ordine = ["Excesiv secetoasă", "Secetoasă", "Moderat secetoasă", "Normală",
          "Umedă", "Foarte umedă", "Excesiv umedă"]
culori = {
    "Excesiv secetoasă": "#7f0000",
    "Secetoasă": "#d7301f",
    "Moderat secetoasă": "#fc8d59",
    "Normală": "#f7f7f7",
    "Umedă": "#91bfdb",
    "Foarte umedă": "#4575b4",
    "Excesiv umedă": "#313695"
}

# 4. Grupare și pivotare
pivot = df.pivot_table(
    index="An",
    columns="Luna",
    values="Clasa_Hellmann",
    aggfunc=lambda x: x.mode().iloc[0] if not x.mode().empty else None
)
pivot = pivot[sorted(pivot.columns)]

# 5. Heatmap categoric
cmap = [culori[c] for c in ordine]
lut = dict(zip(ordine, cmap))
heatmap_data = pivot.replace(lut)

plt.figure(figsize=(10, 12))
sns.heatmap(
    heatmap_data.applymap(lambda x: list(lut.values()).index(x) if x in lut.values() else None),
    cmap=cmap,
    cbar=False,
    linewidths=0.2,
    linecolor='white'
)

plt.title("Calendar Hellmann al secetei și umidității în Câmpia Bărăganului (1961–2020)", fontsize=13)
plt.xlabel("Lună")
plt.ylabel("An")

# 6. Legendă sub eticheta axei „Lună”
patches = [mpatches.Patch(color=culori[k], label=k) for k in ordine]
plt.legend(
    handles=patches,
    title="Clasificare Hellmann",
    loc='upper center',
    bbox_to_anchor=(0.5, -0.04),  # sub „Lună”
    ncol=4,
    frameon=True,
    fancybox=False,
    borderpad=0.8,
    edgecolor='black'
)

# Nu folosim tight_layout pentru a păstra spațiul sub axa X
plt.savefig("grafic_calendar_hellmann_categorie_baragan.png", dpi=300, bbox_inches='tight')
plt.show()
