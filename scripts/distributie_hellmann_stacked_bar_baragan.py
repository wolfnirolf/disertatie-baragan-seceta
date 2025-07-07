import pandas as pd
import matplotlib.pyplot as plt

# 1. Încărcare date
df = pd.read_excel("Date-6statii-precipitatii.xlsx")
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
culori_rb = {
    "Excesiv secetoasă": "#7f0000",
    "Secetoasă": "#d7301f",
    "Moderat secetoasă": "#fc8d59",
    "Normală": "#f7f7f7",
    "Umedă": "#91bfdb",
    "Foarte umedă": "#4575b4",
    "Excesiv umedă": "#313695"
}

# 4. Grupare
grup = df.groupby(["An", "Clasa_Hellmann"]).size().unstack(fill_value=0)
grup = grup[ordine]

# 5. Plot
plt.figure(figsize=(13, 6))
bottom = pd.Series([0]*len(grup), index=grup.index)

for clasa in ordine:
    plt.bar(grup.index, grup[clasa], bottom=bottom, label=clasa, color=culori_rb[clasa])
    bottom += grup[clasa]

plt.title("Distribuția anuală a clasificărilor Hellmann în Câmpia Bărăganului (1961–2020)", fontsize=13)
plt.ylabel("Număr luni clasificate")
plt.xlabel("Anul")
plt.xticks(grup.index, rotation=90, fontsize=8, fontweight='bold')
plt.yticks(fontsize=9)
plt.grid(axis='y', linestyle=':', alpha=0.4)
plt.legend(title="Clasificare Hellmann", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
plt.savefig("grafic_distributie_hellmann_stacked_bar_baragan.png", dpi=300)
plt.show()
