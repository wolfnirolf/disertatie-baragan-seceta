import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Încarcă datele
df = pd.read_excel("Rezultate_SPI3_SPEI3_6statii.xlsx")

# 2. Atribuie anotimpul pe baza lunii
def get_anotimp(luna):
    if luna in [12, 1, 2]:
        return "Iarnă"
    elif luna in [3, 4, 5]:
        return "Primăvară"
    elif luna in [6, 7, 8]:
        return "Vară"
    else:
        return "Toamnă"

df["Anotimp"] = df["Luna"].apply(get_anotimp)

# 3. Atribuie perioada
df["Perioadă"] = df["An"].apply(lambda x: "1961–1990" if x <= 1990 else "1991–2020")

# 4. Diferența SPI - SPEI
df["Dif_SPI_SPEI"] = df["SPI-3"] - df["SPEI-3"]

# 5. Calculează medii pe anotimp și perioadă
grouped = df.groupby(["Perioadă", "Anotimp"])["Dif_SPI_SPEI"].mean().reset_index()

# 6. Ordine anotimpuri
anotimpuri = ["Primăvară", "Vară", "Toamnă", "Iarnă"]
grouped["Anotimp"] = pd.Categorical(grouped["Anotimp"], categories=anotimpuri, ordered=True)
grouped = grouped.sort_values(["Anotimp", "Perioadă"])

# 7. Culoare personalizată
culori = {
    "1961–1990": "#005288",  # albastru închis
    "1991–2020": "#F57C00"   # portocaliu intens
}

# 8. Plot
fig, ax = plt.subplots(figsize=(12, 6))
bar_width = 0.35
x = np.arange(len(anotimpuri))

for perioada, offset in zip(["1961–1990", "1991–2020"], [-bar_width/2, bar_width/2]):
    valori = grouped[grouped["Perioadă"] == perioada]["Dif_SPI_SPEI"].values
    bars = ax.bar(x + offset, valori, width=bar_width, label=perioada, color=culori[perioada])
    
    # Etichete numerice
    for rect in bars:
        val = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2, val + 0.005*np.sign(val),
                f"{val:.2f}", ha='center', va='bottom' if val >= 0 else 'top',
                fontsize=9, color="#003049" if perioada == "1961–1990" else "#5e0000")

# 9. Stilizare
ax.set_xticks(x)
ax.set_xticklabels(anotimpuri, fontsize=11)
ax.set_ylabel("Diferență medie SPI–SPEI", fontsize=12)
ax.set_xlabel("Anotimp", fontsize=12)
ax.set_title("Comparația Diferențelor SPI–SPEI între Perioadele 1961–1990 și 1991–2020", fontsize=14)
ax.axhline(0, color='gray', linestyle='--', linewidth=1)
ax.yaxis.grid(True, linestyle='--', linewidth=0.5, alpha=0.4)
ax.legend(title="Perioadă", title_fontsize=11, fontsize=10)

plt.tight_layout()
plt.savefig("grafic_spi_spei_diferente_perioade.png", dpi=300)
plt.show()
