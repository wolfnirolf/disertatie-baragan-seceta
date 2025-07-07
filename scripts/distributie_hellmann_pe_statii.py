import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_excel("Date-6statii-precipitatii.xlsx")
df.rename(columns={"An_numeric": "An", "Luna_numeric": "Luna"}, inplace=True)

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

ordine = ["Excesiv secetoasă", "Secetoasă", "Moderat secetoasă", "Normală",
          "Umedă", "Foarte umedă", "Excesiv umedă"]

# Noua paletă roșu-albastru
culori_rb = {
    "Excesiv secetoasă": "#67000d",
    "Secetoasă": "#cb181d",
    "Moderat secetoasă": "#fb6a4a",
    "Normală": "#f0f0f0",
    "Umedă": "#74a9cf",
    "Foarte umedă": "#2b8cbe",
    "Excesiv umedă": "#045a8d"
}

df["Clasa_Hellmann"] = df["precip_total"].apply(clasificare_hellmann)

distributie_count = df.groupby(["Statie", df["Clasa_Hellmann"]]).size().unstack(fill_value=0)
distributie_pct = distributie_count.div(distributie_count.sum(axis=1), axis=0) * 100
distributie_pct = distributie_pct[ordine]

plt.figure(figsize=(14, 6))
bottom = np.zeros(len(distributie_pct))

for clasa in ordine:
    valori = distributie_pct[clasa].values
    plt.bar(distributie_pct.index, valori, bottom=bottom, label=clasa, color=culori_rb[clasa])
    bottom += valori

plt.title("Distribuția procentuală a clasificărilor Hellmann pe stații meteorologice (Câmpia Bărăganului)", fontsize=13)
plt.ylabel("Procent (%)")
plt.xlabel("Stație")
plt.xticks(rotation=45, ha="right", fontsize=9, fontweight="bold")
plt.yticks(fontweight="bold")
plt.ylim(0, 100)
plt.legend(title="Clasificare Hellmann", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()

plt.savefig("grafic_distributie_clasificari_hellmann_pe_statii.png", dpi=300)
plt.show()
