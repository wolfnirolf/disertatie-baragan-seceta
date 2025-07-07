import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Încarcă datele
fisier_date = "Rezultate_SPI3_SPEI3_6statii.xlsx"
df = pd.read_excel(fisier_date)

# Filtrare pentru lunile semestrului rece (noiembrie–martie)
df = df[df["Luna"].isin([11, 12, 1, 2, 3])]

# Calculează mediile pe stații
medii = df.groupby("Statie")[["SPI-3", "SPEI-3"]].mean().reset_index()

# Configurare poziții și dimensiuni
bar_width = 0.35
x = np.arange(len(medii["Statie"]))
fig, ax = plt.subplots(figsize=(14, 6))

# Bare colorate
b1 = ax.bar(x - bar_width/2, medii["SPEI-3"], width=bar_width, label="SPEI-3", color="#005288")  # albastru închis
b2 = ax.bar(x + bar_width/2, medii["SPI-3"], width=bar_width, label="SPI-3", color="#F57C00")   # portocaliu

# Etichete numerice lângă capătul barelor (mai apropiate)
for rect in b1:
    height = rect.get_height()
    offset = 0.015 if height >= 0 else -0.025
    ax.text(rect.get_x() + rect.get_width()/2,
            height + offset,
            f'{height:.2f}', ha='center', va='center', fontsize=8, color='#003049')

for rect in b2:
    height = rect.get_height()
    offset = 0.015 if height >= 0 else -0.025
    ax.text(rect.get_x() + rect.get_width()/2,
            height + offset,
            f'{height:.2f}', ha='center', va='center', fontsize=8, color='#5e0000')

# Configurare axă X și Y
ax.set_xticks(x)
ax.set_xticklabels(medii["Statie"], rotation=45, ha="right")
ax.set_ylabel("Valori medii (1961–2020)", fontsize=11)
ax.set_title("Compararea valorilor medii SPEI-3 și SPI-3 în Semestrul Rece (1961–2020)", fontsize=13)

# Linie orizontală zero
ax.axhline(0, color='gray', linewidth=1, linestyle='--')

# Grilaj Y discret
ax.yaxis.grid(True, linestyle='--', linewidth=0.5, alpha=0.4)

# Legenda
ax.legend(title="Indicator")

# Optimizare spațiere și salvare
plt.tight_layout()
plt.savefig("grafic_spi_spei_semestru_rece.png", dpi=300)
plt.show()
